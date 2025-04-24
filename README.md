# Inswags - Django Application Deployment Guide

This guide will help you deploy the Inswags Django application to DigitalOcean App Platform.

## Prerequisites

- A DigitalOcean account
- A GitHub account
- Git installed on your local machine

## Deployment Steps

1. **Fork or push this repository to your GitHub account**

   Update the `.do/app.yaml` file with your GitHub username:
   ```yaml
   github:
     branch: main
     deploy_on_push: true
     repo: your-github-username/Inswags
   ```

2. **Create a new App on DigitalOcean App Platform**

   - Go to the [DigitalOcean Cloud Control Panel](https://cloud.digitalocean.com/)
   - Click on "Apps" in the left sidebar
   - Click "Create App"
   - Select "GitHub" as the source
   - Connect your GitHub account if not already connected
   - Select your repository (Inswags)
   - Select the branch you want to deploy (main)
   - Click "Next"

3. **Configure your App**

   - The App Platform will detect that this is a Python application
   - It will automatically use the settings from your `.do/app.yaml` file
   - Review the settings and make any necessary adjustments
   - Click "Next"

4. **Add a Database**

   - In the "Resources" section, click "Add Resource"
   - Select "Database"
   - Choose "Dev Database" for development or "Production Database" for production
   - Click "Create and Attach"

5. **Set Environment Variables**

   The following environment variables are already configured in the app.yaml file:
   - `DEBUG`: Set to "False" for production
   - `SECRET_KEY`: Will be automatically set from DigitalOcean's environment
   - `DATABASE_URL`: Will be automatically set to connect to your database
   - `ALLOWED_HOSTS`: Will be automatically set to your app's domain

6. **Deploy your App**

   - Review all settings
   - Click "Create Resources"
   - Wait for the deployment to complete

7. **Access your App**

   Once the deployment is complete, you can access your app at the URL provided by DigitalOcean.

## Local Development

To run this application locally:

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```
   python manage.py migrate
   ```

3. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

4. Run the development server:
   ```
   python manage.py runserver
   ```

## Project Structure

- `Ausgeswagt/`: Main Django project directory
- `swags/`: Django app directory
- `templates/`: HTML templates
- `static/`: Static files (CSS, JavaScript, images)
- `media/`: User-uploaded files
- `.do/`: DigitalOcean App Platform configuration
- `Procfile`: Defines the command to run on the server
- `runtime.txt`: Specifies the Python version
- `requirements.txt`: Lists all Python dependencies

## Additional Resources

- [DigitalOcean App Platform Documentation](https://docs.digitalocean.com/products/app-platform/)
- [Django Documentation](https://docs.djangoproject.com/)
- [How to Deploy Django to App Platform Tutorial](https://www.digitalocean.com/community/tutorials/how-to-deploy-django-to-app-platform)