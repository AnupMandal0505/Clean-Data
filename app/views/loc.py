from django.shortcuts import render,redirect
import pandas as pd
import tempfile
from app.models import Csv
import os
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required


@login_required(login_url='signin')
def loc(request,id):
    
    if request.method == 'POST':
        form_data = {}

        for key in request.POST.keys():
            if key.startswith('loc_data_'):
                form_data[key.replace('loc_data_', '')] = request.POST[key]
        # Now form_data contains the dictionary with input values
        # You can use it as needed
        print(form_data)

        filled_values = []

        for key, value in form_data.items():
            if value != '':
                filled_values.append((key, value))

        keys_list = [item[0] for item in filled_values]
        values_list = [item[1] for item in filled_values]
        # new_ls = tuple(int(x) if x.isdigit() else x for x in values_list)

        # print("1st =", keys_list)
        # print("2nd =", values_list)
        # Read CSV file


        obj=Csv.objects.get(id=id)
        df = pd.read_csv(obj.old_csv)
        
        
        # old_columns=list(df.columns)

        # # Create a dictionary mapping old column names to new column names
        # column_mapping = dict(zip(old_columns, new_columns))

        df.set_index(keys_list,inplace=True)
        df.loc[(104)]
            
        print(df)
        if df.empty:
            return render(request, "error.html", {'error_message': 'Uploaded CSV file is empty.'})


        # if not new_columns:
        #     return render(request, "error.html", {'error_message': 'No columns selected for renaming.'})
        



        # new_csv_path = 'Upload/old_csv_file/'
        # file_name = str(id)  # Convert id to string and append '.csv' extension
        # file_path = os.path.join(new_csv_path, file_name)
        # a=df.to_csv(file_path, index=False)
        # # # Update the 'old_csv' field value with the path of the modified CSV file
        # obj.old_csv.name = file_path
        # obj.save()
        
        return redirect('show_data', id=obj)
    else:
        try:
            # Read CSV file using pandas
            obj=Csv.objects.get(id=id)
            df = pd.read_csv(obj.old_csv)
            # Check if the DataFrame is empty
            if df.empty:
                return render(request, "error.html", {'error_message': 'Uploaded CSV file is empty.'})

            # Convert DataFrame to dictionary
            data = df.to_dict(orient='records')

            return render(request, "loc.html",{'data': data,'id':obj})
        except Exception as e:
            return render(request, "error.html", {'error_message': str(e)})
