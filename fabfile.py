from fabric.api import lcd, local

def deploy():
      with lcd('~/Projects/handbook/programmers_handbook'):
          local('git pull')
          local('python manage.py migrate handbook')
          local('python manage.py test handbook')
          local('python manage.py runserver')
