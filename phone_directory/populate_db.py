import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phone_directory.settings')
import django
django.setup()

from contacts.models import Contact
from accounts.models import User


from faker import Faker
fake = Faker('en_IN')


def populate(N=10,CN=2):
    for i in range(N):
        phone = fake.phone_number()
        name = fake.name()
        email = fake.email() if i % 3 == 0 else None
        password = 'Pass@123' #set a simple & common password for all
        user, created = User.objects.get_or_create(phone=phone, defaults={
            'name': name,
            'phone': phone,
            'email': email,
            'password': password
        })
        if created:
            user.set_password(password)
            user.save()
            for j in range(CN):
                label=fake.job()
                phone=fake.phone_number()
                contact = Contact.objects.create(phone=phone,label=label)
                User.objects.addContact(user,contact)
            


if __name__ == '__main__':
    print('Populating data...')
    populate(200,3)
    print('Populating complete')
