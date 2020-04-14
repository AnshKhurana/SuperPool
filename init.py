from accounts.models import User
from pool.models import Group, GroupMember, Category, ShoppingService, FoodService, TravelService, ServiceMember, \
    ServiceGroup
from pool.models import Company, Restaurant

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

# create new services
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

foodv1 = Restaurant(name='McDonald')
foodv1.save()
sf1 = FoodService(category=Category.objects.get(name='Food'), initiator=u2, vendor=foodv1,
                  description="French fries",
                  start_time="2020-01-22 01:01", end_time="2020-01-23 01:01")

sf1.save()

# add initiator as member
sm2 = ServiceMember(service=sf1, user=u2)
sm2.save()

# add service to all groups of the user
gs3 = ServiceGroup(group=g2, service=sf1)
gs3.save()

# Artifically add some more users to the service

sm3 = ServiceMember(service=sf1, user=u1)
sm3.save()
sm4 = ServiceMember(service=ss1, user=u3)
sm4.save()
