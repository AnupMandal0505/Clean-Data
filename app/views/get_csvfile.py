import csv
from django.shortcuts import render,redirect
import pandas as pd
import os
from app.models import User,Csv
import random
from django.contrib.auth.decorators import login_required

def unique_number(name):
    name=name
    while(True):  
        uq=random.randint(1000,9999)
        uq=name+str(uq)
        try:
            n=Csv.objects.get(old_csv=uq)
        except:
            return uq

@login_required(login_url='signin')
def upload_csv(request):
    try:
        csv_file = request.FILES['csv_file']
        # Assuming the CSV file has a header row

        user = request.user
        # Rename the file
        rename=unique_number(user.username)
        csv_file.name = f'{rename}.csv'
    
         # Save file to the user's model instance
        CsvSave=Csv.objects.create(user=user,File_description=csv_file.name,id=csv_file.name)
        CsvSave.old_csv.save(csv_file.name, csv_file)
        return redirect('dasboard')

        # try:
        #     # print(45)
        #     # Read CSV file using pandas
        #     id=Csv.objects.get(id="anurag9877.csv")
        #     df = pd.read_csv(id.old_csv)
            
        #     # Check if the DataFrame is empty
        #     if df.empty:
        #         return render(request, "error.html", {'error_message': 'Uploaded CSV file is empty.'})

        #     # Convert DataFrame to list of dictionaries
        #     data = df.to_dict(orient='records')
        #     # print(789)
        #     return render(request, "show_data.html", {'data': data,'id':id})
        # except Exception as e:
        #     return render(request, "error.html", {'error_message': str(e)})
        
    except Exception as e:
        return render(request, "file_upload.html")




@login_required(login_url='signin')
def merged_csv(request):
    try:
        if request.method == 'POST' and request.FILES.getlist('csv_file'):
            uploaded_files = request.FILES.getlist('csv_file')
            # Initialize an empty DataFrame
            merged_df = pd.DataFrame()
            for uploaded_file in uploaded_files:
                # Read the content of each CSV file
                df = pd.read_csv(uploaded_file)

                # Merge the data from the CSV file into the merged DataFrame
                merged_df = pd.concat([merged_df, df], ignore_index=True)



            csv_file=merged_df
            user = request.user
            # Rename the file
            rename=unique_number(user.username)
            csv_file.name = f'{rename}.csv'
            
            # Save file to the user's model instance
            CsvSave=Csv.objects.create(user=user,File_description=csv_file.name,id=csv_file.name)

            new_csv_path = 'Upload/old_csv_file/'
            # file_name = str(id)  # Convert id to string and append '.csv' extension
            file_path = os.path.join(new_csv_path, csv_file.name)
            a=merged_df.to_csv(file_path, index=False)
            # # Update the 'old_csv' field value with the path of the modified CSV file
            CsvSave.old_csv.name = file_path
            CsvSave.save()

            # CsvSave.old_csv.save(csv_file.name, merged_df.to_csv(csv_file.name, index=False))
            return redirect('dasboard')

    except Exception as e:
        # Handle any exceptions
        error_message = "An error occurred while processing the CSV files. Please try again."
        return render(request, "merged_csv.html", {'error_message': error_message})

    # Render the merged_csv.html template
    return render(request, "merged_csv.html")