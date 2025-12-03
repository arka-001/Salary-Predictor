from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from sklearn.linear_model import LinearRegression
from django.db.models import Avg
from .models import SalaryData

# --- GLOBAL AI MODEL ---
ai_model = LinearRegression()
model_is_trained = False # Flag to track status

# --- HELPER: TRAIN AI ---
def train_ai():
    """
    Trains the global Linear Regression model.
    """
    global ai_model, model_is_trained
    dataset = SalaryData.objects.all()

    # 1. CHECK: Do we have enough data?
    # Linear Regression needs at least 1 row (ideally 2+)
    if not dataset.exists():
        print("⚠ Database Empty. AI cannot train.")
        model_is_trained = False
        return

    # 2. TRAIN
    try:
        df = pd.DataFrame(list(dataset.values('years', 'job_level', 'salary')))
        ai_model.fit(df[['years', 'job_level']], df['salary'])
        model_is_trained = True
        print(f"✅ AI Retrained on {len(df)} rows")
    except Exception as e:
        print(f"Error training AI: {e}")
        model_is_trained = False

# Initialize on startup
train_ai()


# --- HTML VIEWS ---
def home(request):
    """
    Renders the home page.
    """
    return render(request, 'index.html')

def train_page(request):
    """
    Renders the training page.
    """
    db_data = SalaryData.objects.all().order_by('years')
    
    context = {
        'dataset': db_data,
    }
    return render(request, 'train.html', context)


# --- API 1: PREDICT ---
class PredictAPI(APIView):
    """
    API endpoint to predict salary.
    """
    def post(self, request, *args, **kwargs):
        if not model_is_trained:
            return Response({'salary': "No Data! Please train me."}, status=status.HTTP_2_0_OK)

        try:
            years = float(request.data.get('years'))
            level = int(request.data.get('level'))
            
            pred = ai_model.predict([[years, level]])[0]
            
            yearly_salary = abs(pred)
            monthly_salary = yearly_salary / 12
            
            return Response({
                'yearly': f"₹ {yearly_salary:,.0f}",
                'monthly': f"₹ {monthly_salary:,.0f}",
                'raw': yearly_salary
            }, status=status.HTTP_200_OK)
        except (ValueError, TypeError) as e:
            return Response({'error': f"Invalid input: {e}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f"An unexpected error occurred: {e}"}, status=status.HTTP_400_BAD_REQUEST)


# --- API 2: ADD DATA ---
class TrainAPI(APIView):
    """
    API endpoint to add new training data.
    """
    def post(self, request, *args, **kwargs):
        try:
            SalaryData.objects.create(
                years = request.data.get('years'),
                job_level = request.data.get('level'),
                salary = request.data.get('salary')
            )
            train_ai()
            return Response({'message': 'Success'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f"Could not add data: {e}"}, status=status.HTTP_400_BAD_REQUEST)


# --- API 3: DELETE DATA ---
class DeleteAPI(APIView):
    """
    API endpoint to delete a data row.
    """
    def post(self, request, *args, **kwargs):
        try:
            row_id = request.data.get('id')
            SalaryData.objects.get(id=row_id).delete()
            train_ai() # Retrain after delete
            return Response({'message': 'Deleted'}, status=status.HTTP_200_OK)
        except SalaryData.DoesNotExist:
            return Response({'error': 'Data not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f"An unexpected error occurred: {e}"}, status=status.HTTP_400_BAD_REQUEST)


# --- API 4: RESTORE DEFAULTS (Button Logic) ---
class ResetAPI(APIView):
    """
    API endpoint to restore the database to a default set of data.
    """
    def post(self, request, *args, **kwargs):
        try:
            # 1. Clear existing data
            SalaryData.objects.all().delete()
            
            # 2. Define the Default Data
            defaults = [
                (1, 1, 300000), 
                (2, 2, 500000), 
                (3, 5, 800000), 
                (4, 5, 1200000), 
                (5, 9, 2500000), 
                (8, 7, 2800000), 
                (10, 10, 5000000)
            ]
            
            # 3. Insert into Database
            for y, l, s in defaults:
                SalaryData.objects.create(years=y, job_level=l, salary=s)
                
            # 4. Retrain AI
            train_ai()
            
            return Response({'message': 'Defaults Loaded'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f"An error occurred while resetting data: {e}"}, status=status.HTTP_400_BAD_REQUEST)

# --- API 5: DELETE ALL DATA ---
class DeleteAllAPI(APIView):
    """
    API endpoint to delete all data.
    """
    def post(self, request, *args, **kwargs):
        try:
            # Get count before deletion
            data_count = SalaryData.objects.count()
            
            # Delete all data
            SalaryData.objects.all().delete()
            
            # Retrain AI (will fail because no data, but that's expected)
            train_ai()
            
            return Response({
                'message': f'Deleted all {data_count} data points',
                'count': data_count
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f"An error occurred while deleting data: {e}"}, status=status.HTTP_400_BAD_REQUEST)


# --- API 6: GET TRAINING STATS ---
class TrainingStatsAPI(APIView):
    """
    API endpoint to get training statistics.
    """
    def get(self, request, *args, **kwargs):
        try:
            data_count = SalaryData.objects.count()
            
            if data_count > 0:
                avg_salary = SalaryData.objects.aggregate(Avg('salary'))['salary__avg']
                avg_experience = SalaryData.objects.aggregate(Avg('years'))['years__avg']
            else:
                avg_salary = 0
                avg_experience = 0

            return Response({
                'data_points': data_count,
                'average_salary': avg_salary,
                'avg_experience': avg_experience,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f"An error occurred while fetching stats: {e}"}, status=status.HTTP_400_BAD_REQUEST)