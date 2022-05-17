from django.views.generic import TemplateView


class LinkView(TemplateView):
    template_name = "main/link.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["uuid"]=self.kwargs["formation_id"]
        return context