
from urllib.request import Request
from django.shortcuts import  redirect,render


from paciente.forms import PacienteForm, PacienteUpdateForm
from paciente.models import Paciente

from django.contrib import messages

# Create your views here.

# def pacientes(request):
#     titulo="Paciente"
#     pacientes= Paciente.objects.all()
#     context={
#         'titulo':titulo,
#         'pacientes':pacientes
        
#     }

#     return render(request,"listar.html",context)

def pacientes_crear(request):
    titulo="Crear Paciente"
    if request.method == "POST":
        form= PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print("Error")
    else:
        form= PacienteForm()
    context={
        "titulo":titulo,
        "form":form
        
    }
    return render(request,'pacientes-crear.html',context)


def pacientes(request, modal_status="hid"):
    titulo="Crear Pacientes"
    pacientes= Paciente.objects.filter(estado="1")

    ###### Cuerpo del modal ##########
    modal_title=""
    modal_txt=""
    modal_submit=""
    ###################################
    pk_paciente = ""
    tipo =None
    form_update=None
    form =PacienteForm()

    if request.method == "POST" and "form-crear" in request.POST:
        form= PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            form= PacienteForm(request.POST)
            messages.error(
                request, "Error al agregar el paciente"
            )

############################## Configuracion modal de eliminacion ###################


    if request.method == "POST" and "form-eliminar" in request.POST:
        modal_status= "show"
        pk_paciente = request.POST["pk"]
        paciente=Paciente.objects.get(id=pk_paciente)

        ###### Cuerpo del mmodal ########
        modal_title = f"eliminar (paciente)"
        modal_txt= f"Eliminar el Paciente"
        modal_submit= "Aceptar"
        ######################################

        tipo="eliminar"
        ############################ Configuracion modal de edicion ###################
    if request.method == "POST" and "form-editar" in request.POST:
        modal_status= "show"
        pk_paciente = request.POST["pk"]
        paciente=Paciente.objects.get(id=pk_paciente)

        ###### Cuerpo del mmodal ########
        modal_title = f"Editar (paciente)"
        modal_submit= "Editar el paciente"
        ######################################

        tipo="editar"
    
        form_update= PacienteUpdateForm(instance=paciente)

############################ Configuracion de eliminacion ###################

    if request.method == "POST" and "modal-confirmar" in request.POST:
        if request.POST["tipo"]=="eliminar":
            paciente = Paciente.objects.filter(id = int(request.POST["modal-pk"])).update(
                estado="0"

            )
            messages.success(
                request, f"Se eliminò el paciente {paciente} exitosamente!"
            )

            return redirect("login")

        if request.POST["tipo"]=="editar":
            pk_paciente = request.POST["modal-pk"]
            paciente=Paciente.objects.get(id=pk_paciente)
            form_update=PacienteUpdateForm(request.POST, instance=paciente)

            if form_update.is_valid():
                form_update.save()

            messages.success(
                request, f"Se editò el paciente {paciente} exitosamente!"
            )
            return redirect("login")
        
            
    context={

        "titulo":titulo,
        "pacientes":pacientes,
        'form':form,

        "modal_status":modal_status,
        "modal_submit":modal_submit,
        "modal_title":modal_title,
        "modal_txt":modal_txt,
        "pk":pk_paciente,
        "tipo":tipo,
        "form_update":form_update
        
    }
    return render(request,'listar.html',context)




