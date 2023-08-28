# Django Production Setup: A Technical Walkthrough

This guide outlines the step-by-step process to configure and utilize the production setup for a Django project. Following these instructions will help you establish a secure and efficient production environment. The technologies that I decided to use to create the setup are:
  - Docker: used to build, deploy and run application containers;
  - PostgreSQL: used as the default database;
  - Nginx: acts as a reverse proxy, receiving HTTP requests and redirecting them to different backend. Also in a website you have not only the dynamic content, but also static files like images, JavaScript files and CSS style sheets and Nginx serve them efficiently;
  - Redis: used as a cache service;
  - uWSGI: a standard web server used to deploy the application in a production environment.

Let's see them in a more detailed way :smiley:

## Project Structure

![Alt text](django_prod_skeleton/static/image_readme/Client_Server_Django_Prod_Skeleton.png)

This diagram shows the request/response cycle of the production environment:
  1. The NGINX web server becomes the gateway, receiving incoming HTTP requests from clients.
  2. NGINX expertly forwards the received requests to the uWSGI server via a UNIX socket.
  3. uWSGI, the intermediary, relays the request from NGINX to Django for processing.
  4. Django, the heart of the application, processes the request and generates an HTTP response, which is then sent back        through NGINX to the client.

The web server NGINX not only serves the request, but also the static and media (the ones that the user maybe can upload) files in production environment. 

## Instructions: Unveiling the Production Magic

Let's unravel the steps necessary to deploy Docker containers and establish your project's production-ready environment! 

### Running Docker 

There are a few steps needed to run the project: 

    docker-compose build

This command will build or rebuilds images in the docker-compose.yml file that contains all the Dockerfile that will automatically creates containers on the Docker platform.

Then you need to run the following command:

    docker-compose up

This command will start and run an entire application on a standalone host that contains multiple services like Django, Nginx, Cache and Db.

Another useful command is:

    docker-compose down -v

This will stop and remove containers, volumes, networks and images created by the "docker-compose up" command.

You can also run this command:

    docker-compose up --build

This will run both the build and the up docker commands.

### Following the Path

Now, let's chart the course for utilizing this Django production setup:

- Within the project, a file named `.env` file houses various environment variables such as:
  
  - `ADMIN_EMAIL`: this variable stores the email address of the admin user. If an exception occurs, Django will send an error message email to this address.
  - `POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD`: these variables determine the database credentials, including the database name, username, and password.

For security reasons, add the  `.env` file to your `.gitignore` to prevent sensitive information exposure.

- In `prod.py` settings file, it is present this setting:

    ```
   ALLOWED_HOSTS = ['your-website.com', 'www.your-website.com']
    ```

  With this setting, we are saying to Django which host/domain names the project can serve, it is used to prevent HTTP Host header attacks; you can find more on [Django documentation](https://docs.djangoproject.com/en/4.2/ref/settings/). 
  
  When deploying, you can directly input your website's hostname if you have a fixed IP address. Otherwise, use localhost, 127.0.0.1, or a chosen hostname, following these steps:
  
    1. For Linux and macOS, edit `/etc/hosts` and add:
       ```
       127.0.0.1 your-website.com www.your-website.com
       ```
    2. On Windows, add the above line to `C:\Windows\System32\drivers\etc`

 - In the `base.py` file, which houses the common settings for production and development environments, define settings for static and media files:
      ```
      STATIC_URL = 'static/' 
      STATIC_ROOT = os.path.join(BASE_DIR, 'static')

      MEDIA_URL = 'media/'
      MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
      ```
    In your NGINX configuration file `config/nginx/default.conf`, add settings to direct NGINX to serve static and media files:
   
      ```
        location /static/ {
            # location of the static files
            alias /code/django_prod_skeleton/static/;
        }

        location /media/ { 
            # location of the media files
            alias /code/django_prod_skeleton/media/;
        }
      ```

    NGINX will now directly serve these files, bypassing uWSGI.

    To collect static files, initiate Docker with:

        docker-compose up
        

   In another shell, at the parent directory, run:

      ```
      docker-compose exec web python /code/django_prod_skeleton/manage.py collectstatic
      ```

    This command aggregates static files from all project applications and places them in the `STATIC_ROOT` directory.
 
 - Before deploying on production, assess the project using Django's system check framework:
   
      ```
      python manage.py check --deploy --settings=django_prod_skeleton.settings.prod
      ```
    This command will return a list of issues that are related to the security settings:

    - One due to the `SECRET_KEY` setting; replace `django-insecure` in the `SECRET_KEY` with random characters. Store this key in the `.env` file and retrieve it using the `os` library:
          
          SECRET_KEY = os.environ.get('SECRET_KEY')
          
    - The other issues are related to `CSRF_COOKIE_SECURE`, `SESSION_COOKIE_SECURE`, `SECURE_SSL_REDIRECT` and you need to put all three of them to `True` to enhance security. To know better about them look at the [Django documentation](https://docs.djangoproject.com/en/4.2/ref/settings/)

    - The last issue is related to this setting `SECURE_HSTS_SECONDS`; this setting is due to the HTTP Strict Transport Security policy that prevents from connecting to a site that has an expired, self-signed or invalid [SSL/TLS cerificate](https://aws.amazon.com/it/what-is/ssl-certificate/#:~:text=SSL%2FTLS%20stands%20for%20secure,using%20the%20SSL%2FTLS%20protocol.). This certificate is the one related to the `Transport Layer Security (TLS)` protocol that is the standard used for serving a website with a secure connection. 
    
      For a real domain, obtain certificates from a `Certificate Authority (CA)` like `Let's Encrypt`, that will give you trusted SSL/TLS certificates for free; look at this page for more information https://letsencrypt.org/getting-started/ 

      For self-signed certificates, there are a few steps that you need to follow to create your own SSL/TLS certificate:
        - First of all, you need to install OpenSSL on your machine and you can do that following this tutorial (for Windows): 
        https://thesecmaster.com/procedure-to-install-openssl-on-the-windows-platform/
        - Once you have installed it, you can create a new certificate and all you need to do is going inside the folder of the project (where you have the `manage.py` file) and run this command: 

        ```
        openssl req -new -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -out MyCertificate.crt -keyout MyKey.key
        ```

        Then you will be prompted to add identifying information to your certificate. You can see a more detailed explanation about it on this page: https://www.linode.com/docs/guides/create-a-self-signed-tls-certificate/
  
  - In the `docker-compose.yml` file, note two commands under the web service, one for development and another for production. Use `python manage.py runserver` for rapid development and feature testing.

## Credits

This project acknowledges the contributions of Antonio Melé's book ["Django 4 By Example"](https://djangobyexample.com/), which greatly influenced the project's development. This resource enabled the application of new knowledge to this project.

Feel free to suggest improvements, and may this setup guide prove beneficial to your project! 😃












