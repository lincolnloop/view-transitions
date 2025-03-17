import random

from django.shortcuts import redirect
from django.views.generic import TemplateView


class ListView(TemplateView):
    template_name = "examples/list.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(items=list("123"), **kwargs)


class AlpineAjaxView(TemplateView):
    template_name = "examples/alpine-ajax.html"
    DEFAULT_ITEMS = [1, 50, 100]

    def get_items(self):
        return self.request.session.get("items") or self.DEFAULT_ITEMS.copy()

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            items=self.get_items(),
            different=self.get_items() != self.DEFAULT_ITEMS,
            **kwargs,
        )

    def post(self, request, *args, **kwargs):
        if "add-item" in request.POST:
            # Add an item with a random number that's not already in the list
            items = self.get_items()
            while True:
                item = random.randint(1, 100)
                if item not in items:
                    break
            items.append(item)
            items.sort()
            self.request.session["items"] = items
        elif "reset" in request.POST:
            # Reset the items to the default
            self.request.session["items"] = self.DEFAULT_ITEMS.copy()
        elif item := request.POST.get("remove-item"):
            # Remove the item with the given name
            items = self.get_items()
            items.remove(int(item))
            self.request.session["items"] = items
        return redirect(".")
