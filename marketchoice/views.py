from django.shortcuts import render
import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
import pickle
import pandas as pd
import pmdarima as pm
import matplotlib.pyplot as plt
import seaborn as sns
import os
from marketchoice.serializers import MarketSerializer
from marketchoice.models import Market
from myauth.models import User
# Create your views here.


class PredictMarketPrice(APIView):
    def post(self, request):

        MONTHS = request.data['months']

        with open('marketchoice/pricePredictionModel.pkl', 'rb') as f:
            model = pickle.load(f)

        path = 'marketchoice/Price.txt'
        df = pd.read_csv(path)
        data = pd.read_csv(path, parse_dates=['date'], index_col='date')

        n_periods = MONTHS
        fitted, confint = model.predict(
            n_periods=n_periods, return_conf_int=True)
        index_of_fc = pd.date_range(
            data.index[-1], periods=n_periods, freq='MS')
        fitted = fitted.reset_index(drop=True)

        # make series for plotting purpose
        fitted_series = pd.Series(fitted, index=index_of_fc)
        lower_series = pd.Series(confint[:, 0], index=index_of_fc)
        upper_series = pd.Series(confint[:, 1], index=index_of_fc)

        # print("Minimum Price:" , round(lower_series.iloc[-1],-1)) # To Print maximum values for nth month
        # print("Average Price:" , round((lower_series.iloc[-1]+upper_series.iloc[-1])/2,-1)) # To Print average values for nth month
        # print("Maximum Price" , round(upper_series.iloc[-1],-1)) # To Print minimum values for nth month

        # print(lower_series) # To Print minimum values for all months
        # print(upper_series) # To Print maximum values for all months

        # import matplotlib.pyplot as plt

        # set style of the plot
        sns.set_style('whitegrid')

        # plot the confidence interval between the upper and lower series
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.fill_between(lower_series.index,
                        lower_series,
                        upper_series,
                        color=sns.color_palette("Greens")[5], alpha=.15, label='Confidence Interval')

        # add month labels for the x-axis
        months = pd.date_range(
            start=lower_series.index[0], end=lower_series.index[-1], freq='MS')
        ax.set_xticks(months)
        ax.set_xticklabels(months.strftime('%b %Y'),
                           rotation=45, ha='right', fontsize=10)

        # add start and end points for the confidence interval
        ci_start = lower_series.idxmax().strftime('%b %Y')
        ci_end = upper_series.idxmax().strftime('%b %Y')

        # add title and legend
        ax.set_title("Forecast of Cotton Prices", fontsize=16)
        ax.legend(fontsize=12)

        # add gridlines and x-axis label
        ax.grid(True)
        ax.set_xlabel('Date', fontsize=12)

        # plt.show()
        # save the plot as pricePrediction.png plt.
        # delete the previous plot before saving the new one
        
        # if os.path.exists('./static/crops/pricePrediction.png'):
        #     os.remove('./static/crops/pricePrediction.png')

        # plt.savefig('./static/crops/pricePrediction.png',
        #             dpi=300, bbox_inches='tight')

        # Requested Variables:

        min_price = round(lower_series.iloc[-1], -1)
        max_price = round(upper_series.iloc[-1], -1)
        avg_price = round((lower_series.iloc[-1]+upper_series.iloc[-1])/2, -1)
        start = lower_series.idxmax().strftime('%b %Y')
        end = upper_series.idxmax().strftime('%b %Y')

        return Response({'min_price': min_price, 'max_price': max_price, 'avg_price': avg_price, 'start': start, 'end': end})

class GetNearestMarkets(APIView):
    def get(self, request):
        latitude, longitude = request.headers['latitude'], request.headers['longitude']
        latitude, longitude = float(latitude), float(longitude)
        filtered_markets = Market.objects.filter(latitude__range=(latitude-0.3, latitude+0.3), longitude__range=(longitude-0.3, longitude+0.3))
        # serialize the data
        serializer = MarketSerializer(filtered_markets, many=True)
        return Response(serializer.data)

class AddNewMarket(APIView):
    def post(self,request):
        token=request.headers['jwt']
        payload=jwt.decode(token,'secret',algorithms=['HS256'])
        user=User.objects.filter(id=payload['id']).first()
        if user.is_superuser==False:
            return Response({'error':'Not allowed','status':'failure'})
        market_name = request.data['name']
        latitude = request.data['latitude']
        longitude = request.data['longitude']
        latitude, longitude = float(latitude), float(longitude)
        market = Market(name=market_name, latitude=latitude, longitude=longitude)
        market.save()
        return Response({'message': 'Market added successfully','status':'success'})