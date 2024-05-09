from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect 
from django.contrib import messages
from django.views import View
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, LoginForm,PredictionForm
from django.contrib.auth.models import User
from django.views.generic import FormView,TemplateView
import numpy as np
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def home(request):
    return render(request, 'HOUSE_ML/home.html')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'HOUSE_ML/signup.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})
    

class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form: AuthenticationForm):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            self.request.session.set_expiry(0)

            self.request.session.modified = True
        return super(CustomLoginView,self).form_valid(form)
    


from django.contrib.auth.decorators import login_required
from django.db import models


@login_required
def predict(request):
    return render(request, 'HOUSE_ML/prediction.html')



from joblib import load
import json




class Prediction(TemplateView):
    template_name = 'HOUSE_ML/prediction.html'

    def __init__(self):
        self.__data_columns = None
        self.__locations = None
        self.__model = None

    def load_artifacts(self):
        with open(r"HOUSE_ML\model\columns.json", 'r') as f:
            self.__data_columns = json.load(f)['data_columns']
            self.__locations = self.__data_columns[3:]

        if self.__model is None:
            with open('HOUSE_ML/model/hpp.joblib', 'rb') as f:
                self.__model = load(f)

        print('Loading Artifacts')

    def get_location(self):
        return self.__locations

    def data_columns(self):
        return self.__data_columns 
    
    def get_location_names(self):
        # Get the location names from your existing method
        global columns
        locations = self.get_location()
        columns = {'columns': []}  # Initialize an empty list under the 'columns' key
        for loc in locations:
            columns['columns'].append(loc)
        return columns

    def get_estimated_price(self, location, sqft, bhk, bath):
        try:
            loc_index = self.__data_columns.index(location.lower())
        except ValueError:
            loc_index = -1

        x = np.zeros(len(self.__data_columns))
        x[0] = int(sqft) if sqft is not None else 0
        x[1] = int(bath) if bath is not None else 0
        x[2] = int(bhk) if bhk is not None else 0
        if loc_index >= 0:
            x[loc_index] = 1

        return round(self.__model.predict([x])[0], 2)
    

@login_required(login_url='login')
def predict_price(request):
    if request.method == 'GET':
        square_feet = request.GET.get('Squareft')
        bhk = request.GET.get('uiBHK')
        bathrooms = request.GET.get('uiBathrooms')
        location = request.GET.get('uiLocations')

        # Validate the input parameters
        if not all([square_feet, bhk, bathrooms, location]):
            prediction = Prediction()
            prediction.load_artifacts()
            locations = prediction.get_location_names()
            return render(request, 'HOUSE_ML/prediction.html', {'columns': locations['columns'], 'error': 'Please provide all the required fields.'})

        try:
            square_feet = int(square_feet)
            bhk = int(bhk)
            bathrooms = int(bathrooms)
        except ValueError:
            return render(request, 'HOUSE_ML/prediction.html', {'error': 'Invalid input: please enter valid numbers for square feet, BHK, and bathrooms.'})

        # Create an instance of the Prediction class
        prediction = Prediction()
        prediction.load_artifacts()

        # Get the estimated price
        price = prediction.get_estimated_price(location, square_feet, bhk, bathrooms)
        print("Predicted", price)

        # Return the estimated price as JSON response instead of rendering the template
        return JsonResponse({'EstimatedPrice': price, 'Area': square_feet, 'BHK': bhk, 'Bath': bathrooms, "Location": location})


def custom_logout(request):
    logout(request)
    return redirect('home')