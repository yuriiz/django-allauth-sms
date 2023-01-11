# django-allauth-sms
django-allauth provider allowing users to log-in with phone number.
## Installation
1. Install django-allauth-sms package.
`pip install git+https://github.com/yuriiz/django-allauth-sms.git`
2. Configure django-allauth. See https://django-allauth.readthedocs.io/en/latest/installation.html
3. Configure django-sms backend. See https://pypi.org/project/django-sms/
4. Add `allauth_sms` to `INSTALLED_APPS`
```
INSTALLED_APPS = {
        ...
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        ...
        'allauth_sms'
        ...
}
```
5. Use "SMS" option at allauth's `account_login` view.
## Running demo
```bash
git clone https://github.com/yuriiz/django-allauth-sms.git
cd django-allauth.sms
pip install requirements.txt
./manage.py migrate
./manage.py runserver
```
Verification codes will be printed to console with `sms.backends.console.SmsBackend`.
