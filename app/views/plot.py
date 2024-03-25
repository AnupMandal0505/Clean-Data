from django.shortcuts import render, HttpResponse
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from app.models import Csv  # Adjust this import according to your app structure

def plot_view(request, id):
    if request.method == 'POST':
        try:
            obj = Csv.objects.get(id=id)
            df = pd.read_csv(obj.old_csv)
            
            # Extracting form data
            selected_column = request.POST.get('selected_column')
            plot_title = request.POST.get('plot_title')
            ylabel = request.POST.get('ylabel')
            xlabel = request.POST.get('xlabel')
            case = request.POST.get('plot_type')
            print(case)

            if selected_column in df.columns:
                dfx = df[selected_column]
                if case == 'area':
                    graph = area_plot(df, plot_title, xlabel, ylabel)
                elif case == 'hist':
                    graph = hist(dfx, plot_title, xlabel, ylabel)
                elif case == '3D_plot':
                    graph = threeD_plot(dfx, plot_title, xlabel, ylabel)
                else:
                    return HttpResponse("Invalid plot type selected.")

                # Pass the encoded graph to your template
                context = {'graph': graph,'id': id}
                return render(request, 'plot.html', context)
            else:
                return HttpResponse("Invalid column selected for plotting.")
        except Csv.DoesNotExist:
            return HttpResponse("CSV does not exist.", status=404)
    else:
        return render(request, 'create_plot.html', {'id': id})

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
