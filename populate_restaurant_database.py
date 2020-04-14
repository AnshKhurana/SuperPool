import os
import django

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'superpool.settings')
# os.chdir('..')
# django.setup()
# import sys
# sys.path.append('.')

from pool.models import Restaurant
import pandas as pd
from pathlib2 import Path

csv_files = os.listdir('scripts/zomato-india-data-set/Mumbai')
base_path = Path('scripts/zomato-india-data-set/Mumbai/')
restaurant_dataset = None
for file in csv_files:
    if restaurant_dataset is None:
        restaurant_dataset = pd.read_csv(str(base_path.joinpath(file)), sep='|')
    else:
        restaurant_dataset = pd.concat([restaurant_dataset, pd.read_csv(str(base_path.joinpath(file)), sep='|')])
        break
restaurant_dataset.reset_index(drop=True, inplace=True)

Restaurant.objects.all().delete()
for record in restaurant_dataset.iterrows():
    record = record[1]
    restaurant = Restaurant(name=record.NAME,
                            price=record.PRICE,
                            cusine_category=record.CUSINE_CATEGORY,
                            city=record.CITY,
                            region=record.REGION,
                            url=record.URL,
                            page_no=record['PAGE NO'],
                            cusine_type=record['CUSINE TYPE'],
                            timing=record.TIMING,
                            rating=record.RATING,
                            votes=record.VOTES)
    restaurant.save()
