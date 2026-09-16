from django.forms import ModelForm, forms

from catalog.models import Product

FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data["name"]
        name_lower = name.casefold()

        for word in FORBIDDEN_WORDS:
            if word in name_lower:
                raise forms.ValidationError(
                    "Название содержит запрещённое слово."
                )

        return name

    def clean_description(self):
        description = self.cleaned_data["description"]

        if description:
            description_lower = description.casefold()

            for word in FORBIDDEN_WORDS:
                if word in description_lower:
                    raise forms.ValidationError(
                        "Описание содержит запрещённое слово."
                    )

        return description

    def clean_price(self):
        price = self.cleaned_data["price"]

        if price < 0:
            raise forms.ValidationError(
                "Цена не может быть отрицательной."
            )

        return price

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

        self.fields["category"].widget.attrs["class"] = "form-select"
