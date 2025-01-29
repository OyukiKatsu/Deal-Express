from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth import login
from django.views import View
from core.models import Profile, Empresa
from .forms import ProfileForm, EmpresaForm, ProfileFormEdit
from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES)
        empresa_form = EmpresaForm(request.POST)
        
        if profile_form.is_valid():
            # Guardar el usuario
            user = profile_form.save(commit=False)
            user.set_password(profile_form.cleaned_data['password'])  # Encripta la contraseña
            user.save()
            
            # Si es una empresa, procesar el formulario de empresa
            if user.is_empresa and empresa_form.is_valid():
                empresa = empresa_form.save()  # Guardar la empresa
                user.empresa_id = empresa  # Asociar el usuario con la empresa creada
                user.save()
            
            # Asignar al grupo correspondiente
            cliente_group, _ = Group.objects.get_or_create(name='Cliente')
            empresa_group, _ = Group.objects.get_or_create(name='Empresa')
            
            if user.is_empresa:
                user.groups.add(empresa_group)  # Empresa
            else:
                user.groups.add(cliente_group)  # Cliente
            
            # Iniciar sesión automáticamente (opcional)
            login(request, user)
            return redirect('index_marketplace')  # Redirigir a una página de éxito
        
    else:
        profile_form = ProfileForm()
        empresa_form = EmpresaForm()
    
    context = {
        'profile_form': profile_form,
        'empresa_form': empresa_form,
    }
    return render(request, 'usuario/registration.html', context)


class ProfileView(DetailView):
    model = Profile  # El modelo es User
    template_name = 'usuario/detalle.html'  # La plantilla que mostrarás
    context_object_name = 'profile'  # Cómo llamarás al objeto que contiene el usuario en la plantilla

    # Este método permite personalizar cómo obtener el usuario
    def get_object(self, queryset=None):
        # El username se pasa como parte de la URL, lo obtenemos usando self.kwargs
        username = self.kwargs['username']
        return Profile.objects.get(username=username)
    
def ProfileEditView(request,*args,**kwargs):
    
    # Obtener el perfil basado en el username
    if kwargs.get('username', None) is None:
        raise NameError("El argumento 'username' es obligatorio")
    username = kwargs['username']
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        if request.POST.get('save_changes', None) == 'guardar':

            profile_form = ProfileFormEdit(request.POST, request.FILES, instance=user.profile)
            if profile_form.is_valid():
                # Actualizar atributos del perfil
                user.username = request.POST.get('username')
                user.profile.correo = request.POST.get('correo')
                user.profile.dni = request.POST.get('dni')

                

                image = request.FILES.get('imagen_perfil')
                if image:
                    user.profile.imagen_perfil = image
                    user.profile.save()
                user.save()
                user.profile.save() 
                
                return redirect('user:editar_perfil', username=user.username)

        elif request.POST.get('deactivate_account', None) == 'delete':
            # Eliminar perfil
            user.delete()   
            return redirect('user:registration')  # Redirigir tras eliminación

    return render(request, 'usuario/edit.html', {'user': user})