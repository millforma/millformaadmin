from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages


# get formation session from cirrushield
class SearchFormation(TemplateView, UserPassesTestMixin):
    template_name = 'main/importcirrus.html'

    def test_func(self):
        return self.request.user.groups.filter(name='commercial').exists()

    def post(self, request):
        num_doss = request.POST.get("num_dossier")
        messages.success(self.request, "Veuillez vérifier les informations ci-dessous")
        return redirect('cirrushieldapi:postformation', formation_id=num_doss)
