import os

from accounts.models import User
from pool.models import Group, GroupMember, Category, ShoppingService, FoodService, TravelService, ServiceMember, \
    ServiceGroup, Location
from pool.models import Company, Restaurant, Message
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

# Restaurant.objects.all().delete()
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
print('Restaurants table created')

# create users

u1 = User.objects.create_user(username='john', email='a@bc.com', phone_number='+1234567890', address='xy',
                              password='Abcd123$')
u1.save()
u2 = User.objects.create_user(username='john2', email='x@bc.com', phone_number='+1234567891', address='xyz',
                              password='Abcd123$')
u2.save()
u3 = User.objects.create_user(username='john3', email='y@bc.com', phone_number='+1234567893', address='xyw',
                              password='Abcd123$')
u3.save()

# create groups
g1 = Group(admin=u1, name='g1', description='d1')
g1.save()
g2 = Group(admin=u2, name='g2', description='d2')
g2.save()
print('Groups created')

# add members to groups
gm1 = GroupMember(group=g1, user=u1)
gm1.save()
gm12 = GroupMember(group=g2, user=u1)
gm12.save()
gm2 = GroupMember(group=g2, user=u2)
gm2.save()
gm3 = GroupMember(group=g1, user=u3)
gm3.save()
gm4 = GroupMember(group=g2, user=u3)
gm4.save()
print('Group Members added')

# initialize categories for services
c1 = Category(name='Food')
c1.save()
c1 = Category(name='Travel')
c1.save()
c1 = Category(name='Shopping')
c1.save()
c1 = Category(name='Event')
c1.save()
c1 = Category(name='Other')
c1.save()
print('Categories added')

# create new services
##--------------------------Shopping----------------------##
comp1 = Company(name="Adidas", domain="Footwear")
comp1.save()
ss1 = ShoppingService(category=Category.objects.get(name='Shopping'), initiator=u1, vendor=comp1,
                      description="Buying the best shoes",
                      start_time="2020-01-01 01:01", end_time="2020-01-01 01:02")
ss1.save()

# add initiator as member
sm1 = ServiceMember(service=ss1, user=u1)
sm1.save()

# add service to all groups of the user
gs1 = ServiceGroup(group=g1, service=ss1)
gs1.save()

gs2 = ServiceGroup(group=g2, service=ss1)
gs2.save()
print('Shopping service created')
##-----------Food--------------------------##
## McDonalds 2 years back
foodv1 = Restaurant(name='McDonald')
foodv1.save()

sf1_old2 = FoodService(category=Category.objects.get(name='Food'), initiator=u2, vendor=foodv1,
                       description="French fries",
                       start_time="2018-01-22 01:01", end_time="2018-01-23 01:01")

sf1_old2.save()

# add initiator as member
sm2_old2 = ServiceMember(service=sf1_old2, user=u2)
sm2_old2.save()

# add service to all groups of the user
gs3_old2 = ServiceGroup(group=g2, service=sf1_old2)
gs3_old2.save()

## McDonalds 1 year back
sf1_old1 = FoodService(category=Category.objects.get(name='Food'), initiator=u2, vendor=foodv1,
                       description="French fries",
                       start_time="2019-01-22 01:01", end_time="2019-01-23 01:01")

sf1_old1.save()

# add initiator as member
sm2_old1 = ServiceMember(service=sf1_old1, user=u2)
sm2_old1.save()

# add service to all groups of the user
gs3_old1 = ServiceGroup(group=g2, service=sf1_old1)
gs3_old1.save()

## McDonalds at recent time
sf1 = FoodService(category=Category.objects.get(name='Food'), initiator=u1, vendor=foodv1,
                  description="French fries",
                  start_time="2020-04-14 01:01", end_time="2020-05-14 01:01")

sf1.save()

# add initiator as member
sm2 = ServiceMember(service=sf1, user=u1)
sm2.save()

# add service to all groups of the user
gs3_1 = ServiceGroup(group=g1, service=sf1)
gs3_1.save()

gs3_2 = ServiceGroup(group=g2, service=sf1)
gs3_2.save()
print('Food Services created')
##--------------Food-------------------------##

loc1 = Location(latitude=19.1334, longitude=72.9133, address='IIT Bombay, Powai, Mumbai-400076',
                timestamp="2020-04-14 00:00")
loc2 = Location(latitude=19.0936, longitude=72.8566, address='Chhatrapati Shivaji International Airport, Mumbai',
                timestamp="2020-04-14 00:00")
loc3 = Location(latitude=18.5538, longitude=73.9048, address='Hyatt, Pune',
                timestamp="2020-04-14 00:00")
loc4 = Location(latitude=28.5562, longitude=77.1000, address='Indira Gandhi International Airport, Delhi',
                timestamp="2020-04-14 00:00")
loc5 = Location(latitude=22.6520, longitude=88.4463, address='Netaji Subhas Chandra Bose, International Airport, '
                                                             'Kolkata',
                timestamp="2020-04-14 00:00")
loc1.save()
loc2.save()
loc3.save()
loc4.save()
loc5.save()

st1 = TravelService(category=Category.objects.get(name='Travel'), initiator=u1, start_point=loc1, end_point=loc2,
                    description="Going to airport", transport='Taxi',
                    start_time="2020-01-22 09:00", end_time="2020-01-23 10:00")

st2 = TravelService(category=Category.objects.get(name='Travel'), initiator=u2, start_point=loc1, end_point=loc4,
                    description="Going to Delhi", transport='Flight',
                    start_time="2020-01-22 09:00", end_time="2020-01-23 10:00")

st3 = TravelService(category=Category.objects.get(name='Travel'), initiator=u3, start_point=loc1, end_point=loc3,
                    description="Going to Pune", transport='Train',
                    start_time="2020-01-22 08:00", end_time="2020-01-23 11:00")

st1.save()
st2.save()
st3.save()

# add initiator as member
smt1 = ServiceMember(service=st1, user=u1)
smt1.save()

smt2 = ServiceMember(service=st2, user=u2)
smt2.save()

smt3 = ServiceMember(service=st3, user=u3)
smt3.save()

# add service to all groups of the user
gst1 = ServiceGroup(group=g1, service=st1)
gst1.save()

gst2 = ServiceGroup(group=g2, service=st1)
gst2.save()

gst3 = ServiceGroup(group=g2, service=st2)
gst3.save()

gst4 = ServiceGroup(group=g1, service=st3)
gst4.save()

gst5 = ServiceGroup(group=g2, service=st3)
gst5.save()
print('Travel Service created')

# Artifically add some more users to the service

sm3 = ServiceMember(service=sf1, user=u1)
sm3.save()
sm4_member2 = ServiceMember(service=ss1, user=u2)
sm4_member2.save()
sm4_member3 = ServiceMember(service=ss1, user=u3)
sm4_member3.save()
sm5 = ServiceMember(service=st2, user=u1)
sm5.save()
print('Members added to service')

m11 = Message(timestamp="2020-01-23 11:00", content="Hi everyone", service=ss1, user=u1)
m11.save()
m21 = Message(timestamp="2020-01-23 11:01", content="Hi", service=ss1, user=u2)
m21.save()
m32 = Message(timestamp="2020-01-23 11:02", content="Where is john3?", service=ss1, user=u2)
m32.save()
m41 = Message(timestamp="2020-01-23 11:03", content="Wait, he is joining", service=ss1, user=u1)
m41.save()
m53 = Message(timestamp="2020-01-23 11:23", content="Hey, Whatsup?", service=ss1, user=u3)
m53.save()
m62 = Message(timestamp="2020-01-23 11:25", content="Goodnight", service=ss1, user=u2)
m62.save()
print('Messages added to chat')
