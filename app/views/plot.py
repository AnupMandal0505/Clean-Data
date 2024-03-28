from django.shortcuts import render, HttpResponse
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from app.models import Csv  # Adjust this import according to your app structure

def plot_view(request, id):
    if request.method == 'POST':
        try:
            # Get list of columns to delete from user input
            columns = request.POST.getlist('column')
            obj = Csv.objects.get(id=id)
            df = pd.read_csv(obj.old_csv)
            
            # Extracting form data
            # selected_column = request.POST.get('selected_column')
            plot_title = request.POST.get('plot_title')
            ylabel = request.POST.get('ylabel')
            xlabel = request.POST.get('xlabel')
            case = request.POST.get('plot_type')
            print(case)

            # if selected_column in df.columns:
            #     dfx = df[selected_column]
            #     if case == 'area':
            #         graph = area_plot(df, plot_title, xlabel, ylabel)
            #     elif case == 'hist':
            #         graph = hist(dfx, plot_title, xlabel, ylabel)
            #     elif case == '3D_plot':
            #         graph = threeD_plot(dfx, plot_title, xlabel, ylabel)
            #     else:
            #         return HttpResponse("Invalid plot type selected.")

            #     # Pass the encoded graph to your template
            #     context = {'graph': graph,'id': id}
            #     return render(request, 'plot.html', context)
            if all(col in df.columns for col in columns):
                dfx = df[columns]
                if case == 'area':
                    graph = area_plot(dfx, plot_title, xlabel, ylabel)
                elif case == 'hist':
                    graph = hist(dfx, plot_title, xlabel, ylabel)
                elif case == '3D_plot':
                    graph = threeD_plot(dfx, plot_title, xlabel, ylabel)
                elif case == 'pie_plot':
                    graph, error = pie_plot(dfx, plot_title)
                    if error:
                        # Handle the error, perhaps by showing it on the page or logging it
                        # return HttpResponse(error)
                        return HttpResponse("Invalid select columns check your columns data numeric data or not!")
                else:
                    return HttpResponse("Invalid plot type selected.")

                # Pass the encoded graph to your template
                context = {'graph': graph, 'id': id}
                return render(request, 'plot.html', context)

            else:
                return HttpResponse("Invalid column selected for plotting.")
        except Csv.DoesNotExist:
            return HttpResponse("CSV does not exist.", status=404)
    else:
        try:
            # Retrieve the Csv object based on the ID
            obj = Csv.objects.get(id=id)

            # Read CSV file into a DataFrame
            df = pd.read_csv(obj.old_csv)

            # Check if the DataFrame is empty
            if df.empty:
                return render(request, "error.html", {'error_message': 'Uploaded CSV file is empty.'})

            # Convert DataFrame to dictionary
            data = df.to_dict(orient='records')
            # print(data)
            return render(request, "create_plot.html",{'data':data,'id':id})
        except Exception as e:
            return render(request, "error.html", {'error_message': str(e)})
        # return render(request, 'create_plot.html', {'id': id})

def area_plot(dfx, title, xlabel, ylabel):
    plt.figure(figsize=(10,6))
    dfx.plot(kind='area')
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    return get_graph()

def hist(dfx, title, xlabel, ylabel):
    plt.figure(figsize=(10,6))
    dfx.hist()
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    return get_graph()

def pie_plot(dfx, title):
    try:
        avg = dfx.mean()
    except Exception as e:
        # Instead of returning, you could log the error or handle it differently
        # print(f"Error generating pie chart: {e}")
        return None, f"Error generating pie chart: {str(e)}  Check your columns data numeric or not"  # Returning error message along with None

    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('equal')
    langs = avg.index.tolist()
    averages = avg.tolist()
    # myexplode = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1]  # Adjusted explode values
    # Calculate the number of columns
    num_columns = len(langs)
    
    # Generate explode values
    explode_step = 0.1 / num_columns  # Adjust this value for more or less separation
    myexplode = [explode_step] * num_columns
    ax.pie(averages, labels=langs, autopct='%1.2f%%', explode=myexplode)
    ax.set_title(title)  # Corrected typo in title
    return get_graph(),None

def threeD_plot(dfx, title, xlabel, ylabel):
    # Assuming dfx contains three columns for x, y, and z coordinates
    fig = plt.figure(figsize=(10,6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(dfx['Mat'], dfx['Inns'], dfx['Runs'])
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel('Z')
    return get_graph()


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    # plt.close()
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph
