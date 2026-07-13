from auth_app.models import CustomUser

def create_test_users():
    business_user = CustomUser.objects.create_user(
        username='max_business',
        email='max@business.de',
        password='password123',
        type='business'
    )
    customer_user = CustomUser.objects.create_user(
        username='customer_jane',
        email='jane@customer.de',
        password='password123',
        type='customer'
    )
    return business_user, customer_user

def assert_profile_fields(response_data, is_business=False):
    for field in ['location', 'tel', 'description', 'working_hours']:
        if is_business or field not in ['working_hours', 'description']:
            assert field in response_data
            assert isinstance(response_data[field], str)