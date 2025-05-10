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

   For Digital Ocean Spaces integration, you'll need to add these additional environment variables:
   - `USE_SPACES`: Set to "True" to enable Digital Ocean Spaces for file storage
   - `SPACES_ACCESS_KEY_ID`: Your Digital Ocean Spaces access key
   - `SPACES_SECRET_ACCESS_KEY`: Your Digital Ocean Spaces secret key
   - `SPACES_BUCKET_NAME`: The name of your Digital Ocean Spaces bucket
   - `SPACES_REGION`: The region of your Digital Ocean Spaces (default is "nyc3")

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

## Setting Up Digital Ocean Spaces

This application can use Digital Ocean Spaces for storing user-uploaded files. Follow these steps to set it up:

1. **Create a Spaces Bucket**
   - Go to the [DigitalOcean Cloud Control Panel](https://cloud.digitalocean.com/)
   - Click on "Spaces" in the left sidebar
   - Click "Create a Space"
   - Select a region (e.g., nyc3)
   - Choose a unique name for your bucket
   - Configure file access (recommended: "Restrict File Listing")
   - Click "Create a Space"

2. **Create Access Keys**
   - In the DigitalOcean Cloud Control Panel, go to "API" in the left sidebar
   - Under "Spaces access keys", click "Generate New Key"
   - Enter a name for your key
   - Copy both the access key and secret key (you won't be able to see the secret key again)

3. **Configure Environment Variables**
   - In your App Platform settings, add the environment variables listed in the "Set Environment Variables" section above
   - Set `USE_SPACES` to "True"
   - Add your access key, secret key, bucket name, and region

4. **CORS Configuration (if needed)**
   - If you're uploading files directly from the browser, you may need to configure CORS
   - In your Space settings, go to the "Settings" tab
   - Under "CORS", add your app's domain to the "Origin" field
   - Set "Allowed Methods" to include at least GET, PUT, POST
   - Click "Save"

## Additional Resources

- [DigitalOcean App Platform Documentation](https://docs.digitalocean.com/products/app-platform/)
- [DigitalOcean Spaces Documentation](https://docs.digitalocean.com/products/spaces/)
- [Django Documentation](https://docs.djangoproject.com/)
- [How to Deploy Django to App Platform Tutorial](https://www.digitalocean.com/community/tutorials/how-to-deploy-django-to-app-platform)
