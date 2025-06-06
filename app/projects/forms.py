import os
import pickle

import numpy as np
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.conf import settings as django_settings
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from dashboard.helpers import KPI_PARAMETERS_ASSETS
from projects.constants import RENEWABLE_ASSETS
from projects.helpers import (
    parameters_helper,
    PARAMETERS,
    DualNumberField,
    parse_input_timeseries,
)
from projects.models import *


def gettext_variables(some_string, lang="de"):
    """Save some expressions to be translated to a temporary file
    Because django makemessages cannot detect gettext with variables
    """

    some_string = str(some_string)

    trans_file = os.path.join(
        django_settings.STATIC_ROOT, f"personal_translation_{lang}.pickle"
    )

    if os.path.exists(trans_file):
        with open(trans_file, "rb") as handle:
            trans_dict = pickle.load(handle)
    else:
        trans_dict = {}

    if some_string is not None:
        if some_string not in trans_dict:
            trans_dict[some_string] = ""

        with open(trans_file, "wb") as handle:
            pickle.dump(trans_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


def set_parameter_info(param_name, field, parameters=PARAMETERS):
    # For the storage unit
    if param_name.split("_")[0] in ("cp", "dchp", "chp"):
        param_name = "_".join(param_name.split("_")[1:])

    help_text = None
    unit = None
    verbose = None
    default_value = None
    if param_name == "optimize_cap":
        param_name = "optimize_capacity"
    if param_name in PARAMETERS:
        help_text = PARAMETERS[param_name][":Definition_Short:"]
        unit = PARAMETERS[param_name][":Unit:"]
        verbose = PARAMETERS[param_name]["verbose"]
        default_value = PARAMETERS[param_name][":Default:"]
        if unit == "None":
            unit = None
        elif unit == "Factor":
            unit = ""
        if verbose == "None":
            verbose = None
        if default_value == "None":
            default_value = None

    if verbose is not None:
        field.label = verbose
    if unit is not None:
        field.label = _(str(field.label)) + " (" + _(unit) + ")"
    else:
        field.label = _(str(field.label))

    if help_text is not None:
        field.help_text = _(help_text)

    if default_value is not None:
        field.initial = default_value


class OpenPlanModelForm(ModelForm):
    """Class to automatize the assignation and translation of the labels, help_text and units"""

    def __init__(self, *args, **kwargs):
        super(OpenPlanModelForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            set_parameter_info(fieldname, field)


class OpenPlanForm(forms.Form):
    """Class to automatize the assignation and translation of the labels, help_text and units"""

    def __init__(self, *args, **kwargs):
        super(OpenPlanForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            set_parameter_info(fieldname, field)


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        exclude = ["id", "rating"]


class ProjectDetailForm(ModelForm):
    class Meta:
        model = Project
        exclude = ["date_created", "date_updated", "economic_data", "user", "viewers"]

    def __init__(self, *args, **kwargs):
        super(ProjectDetailForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True


class EconomicDataDetailForm(OpenPlanModelForm):
    class Meta:
        model = EconomicData
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(EconomicDataDetailForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True


economic_widgets = {
    "discount": forms.NumberInput(
        attrs={
            "placeholder": _("eg. 0.1"),
            "min": "0.0",
            "max": "1.0",
            "step": "0.0001",
            "title": _("Investment Discount factor."),
        }
    ),
    "tax": forms.NumberInput(
        attrs={"placeholder": "eg. 0.3", "min": "0.0", "max": "1.0", "step": "0.0001"}
    ),
}


class EconomicDataUpdateForm(OpenPlanModelForm):
    class Meta:
        model = EconomicData
        fields = "__all__"
        widgets = economic_widgets


class ProjectCreateForm(OpenPlanForm):
    name = forms.CharField(
        label=_("Project Name"),
        widget=forms.TextInput(
            attrs={
                "placeholder": "Name...",
                "data-bs-toggle": "tooltip",
                "title": _("A self explanatory name for the project."),
            }
        ),
    )
    description = forms.CharField(
        label=_("Project Description"),
        widget=forms.Textarea(
            attrs={
                "placeholder": "More detailed description here...",
                "data-bs-toggle": "tooltip",
                "title": _(
                    "A description of what this project objectives or test cases."
                ),
            }
        ),
    )
    country = forms.ChoiceField(
        label=_("Country"),
        choices=COUNTRY,
        widget=forms.Select(
            attrs={
                "data-bs-toggle": "tooltip",
                "title": _("Name of the country where the project is being deployed"),
            }
        ),
    )
    longitude = forms.FloatField(
        label=_("Location, longitude"),
        widget=forms.NumberInput(
            attrs={
                "placeholder": "click on the map",
                "readonly": "",
                "data-bs-toggle": "tooltip",
                "title": _(
                    "Longitude coordinate of the project's geographical location."
                ),
            }
        ),
    )
    latitude = forms.FloatField(
        label=_("Location, latitude"),
        widget=forms.NumberInput(
            attrs={
                "placeholder": "click on the map",
                "readonly": "",
                "data-bs-toggle": "tooltip",
                "title": _(
                    "Latitude coordinate of the project's geographical location."
                ),
            }
        ),
    )
    # duration = forms.IntegerField(
    #     label=_("Project Duration"),
    #     widget=forms.NumberInput(
    #         attrs={
    #             "placeholder": "eg. 1",
    #             "min": "0",
    #             "max": "100",
    #             "step": "1",
    #             "data-bs-toggle": "tooltip",
    #             "title": _(
    #                 "The number of years the project is intended to be operational. The project duration also sets the installation time of the assets used in the simulation. After the project ends these assets are 'sold' and the refund is charged against the initial investment costs."
    #             ),
    #         }
    #     ),
    # )
    currency = forms.ChoiceField(
        label=_("Currency"),
        choices=CURRENCY,
        widget=forms.Select(
            attrs={
                "data-bs-toggle": "tooltip",
                "title": _(
                    "The currency of the country where the project is implemented."
                ),
            }
        ),
    )
    # discount = forms.FloatField(
    #     label=_("Discount Factor"),
    #     widget=forms.NumberInput(
    #         attrs={
    #             "placeholder": "eg. 0.1",
    #             "min": "0.0",
    #             "max": "1.0",
    #             "step": "0.0001",
    #             "data-bs-toggle": "tooltip",
    #             "title": _(
    #                 "Discount factor is the factor which accounts for the depreciation in the value of money in the future, compared to the current value of the same money. The common method is to calculate the weighted average cost of capital (WACC) and use it as the discount rate."
    #             ),
    #         }
    #     ),
    # )
    # tax = forms.FloatField(
    #     label=_("Tax"),
    #     widget=forms.NumberInput(
    #         attrs={
    #             "placeholder": "eg. 0.3",
    #             "min": "0.0",
    #             "max": "1.0",
    #             "step": "0.0001",
    #             "data-bs-toggle": "tooltip",
    #             "title": _("Tax factor"),
    #         }
    #     ),
    # )
    unit_choice = forms.ChoiceField(
        choices=MW_KW_CHOICE,
        widget=forms.Select(
            attrs={
                "data-bs-toggle": "tooltip",
                "title": _(""),
            }
        ),
    )
    unit_choice_co2 = forms.ChoiceField(
        choices=CO2_UNIT_CHOICE,
        widget=forms.Select(
            attrs={
                "data-bs-toggle": "tooltip",
                "title": _(""),
            }
        ),
    )

    # Render form
    def __init__(self, *args, **kwargs):
        super(ProjectCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "project_form_id"
        # self.helper.form_class = 'blueForm'
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Submit"))

        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-lg-8"
        self.helper.field_class = "col-lg-10"
        self.fields["unit_choice"].label = (
            "Unit Choice for all Scenarios of the Project - Please ensure that all technology parameters have the same unit prefix"
        )
        self.fields["unit_choice_co2"].label = "Unit Choice for CO2 amounts"


class ProjectUpdateForm(OpenPlanModelForm):
    class Meta:
        model = Project
        exclude = ["date_created", "date_updated", "economic_data", "user", "viewers"]

    def __init__(self, *args, **kwargs):
        super(ProjectUpdateForm, self).__init__(*args, **kwargs)
        self.fields["unit_choice"].label = (
            "Unit Choice for all Scenarios of the Project - Please ensure that all technology parameters have the same unit prefix"
        )
        self.fields["unit_choice_co2"].label = "Unit Choice for CO2 amounts"


class ProjectShareForm(ModelForm):
    email = forms.EmailField(label=_("Email address"))

    class Meta:
        model = Viewer
        exclude = ["id", "user"]


class ProjectRevokeForm(ModelForm):
    class Meta:
        model = Project
        fields = ["viewers"]
        widgets = {"viewers": forms.SelectMultiple()}
        help_texts = {
            "viewers": _(
                "Select the user(s) for which you want to revoke access rights "
            )
        }
        labels = {"viewers": _("Users currently having access to the project")}

    def __init__(self, *args, **kwargs):
        proj_id = kwargs.pop("proj_id", None)
        super().__init__(*args, **kwargs)
        self.fields["viewers"].empty_label = _("No users have access to this project")
        self.fields["viewers"].required = False
        if proj_id is not None:
            self.fields["viewers"].queryset = Project.objects.get(
                id=proj_id
            ).viewers.all()


class UploadFileForm(forms.Form):
    name = forms.CharField(required=False)
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        labels = kwargs.pop("labels", None)
        super().__init__(*args, **kwargs)
        if labels is not None:
            for field in labels:
                self.fields[field].label = _(labels[field])


class UseCaseForm(forms.Form):
    usecase = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        usecase_qs = kwargs.pop("usecase_qs")
        usecase_url = kwargs.pop("usecase_url", "usecase_url")
        super().__init__(*args, **kwargs)
        if usecase_qs is not None:
            self.fields["usecase"].choices = [(uc.id, uc.name) for uc in usecase_qs]
            self.fields["usecase"].label = (
                _("Select a use case (or")
                + f"<a href='{usecase_url}'>"
                + _(" visit use cases page link")
                + "</a>)"
            )


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ["id", "project"]


# region Scenario
# TODO build this from the documentation with a for loop over the keys
scenario_widgets = {
    "name": forms.TextInput(attrs={"placeholder": "Scenario name"}),
    "start_date": forms.DateInput(
        format="%Y-%m-%d",
        attrs={
            "class": "TestDateClass",
            "placeholder": "Select a start date",
            "type": "date",  # The standard HTML5 input tag type="date" doesn’t allow for customization.
        },
    ),
    "time_step": forms.Select(
        attrs={
            "placeholder": "eg. 120 minutes",
            "min": "1",
            "max": "600",
            "step": "1",
            "data-bs-toggle": "tooltip",
            "title": _("Length of the time-steps."),
        },
        choices=((60, "60 min"), (15, "15 min")),
    ),
    "evaluated_period": forms.NumberInput(
        attrs={
            "placeholder": "so far only one year is possible",
            "min": "365",
            "max": "365",
            "step": "1",
            "data-bs-toggle": "tooltip",
            "title": _("The number of days simulated with the energy system model."),
            # "onchange": "getEvaluatedPeriod(this.value)"
        }
    ),
    "interest_rate": forms.NumberInput(
        attrs={
            "placeholder": "",
            "min": "0",
            "data-bs-toggle": "tooltip",
            "title": _(
                "interest rate in % - is used for the interest calculation of the annuities of the technologies"
            ),
        }
    ),
    "simulation_year": forms.Select(
        attrs={
            "placeholder": "eg. 2035",
            "step": "5",
            "data-bs-toggle": "tooltip",
            "title": _("Simulationyear"),
        },
        choices=(
            (2025, "2025"),
            (2030, "2030"),
            (2035, "2035"),
            (2040, "2040"),
            (2045, "2045"),
            (2050, "2050"),
        ),
    ),
    "user_mode_choice": forms.Select(
        attrs={
            "placeholder": "",
            "data-bs-toggle": "tooltip",
            "title": _("user_mode_choice"),
        },
        choices=(("Default User", "Default User"), ("Expert", "Expert")),
    ),
    # "timeframe_choice": forms.Select(
    #     choices=TIME_CHOICE,
    #     attrs={
    #         "placeholder": "Choose your wanted time frame",
    #         "data-bs-toggle": "tooltip",
    #         "title": _(""),
    #         "onchange": "getTimeframeChoice(this.value)",
    #     }
    # ),
    # "capex_fix": forms.NumberInput(
    #     attrs={
    #         "placeholder": "e.g. 10000€",
    #         "min": "0",
    #         "data-bs-toggle": "tooltip",
    #         "title": _(
    #             "A fixed cost to implement the asset, eg. planning costs which do not depend on the (optimized) asset capacity."
    #         ),
    #     }
    # ),
}

scenario_labels = {
    "project": _("Project"),
    "name": _("Scenario name"),
    "evaluated_period": _(
        "Simulation period of one year"
    ),  # (Note that a very short simulation period can lead to unrealistic results.)
    "time_step": _("Time Step"),
    "start_date": _("Start Date"),
    # "capex_fix": _("Development costs"),
    # "timeframe_choice": _(""),
    "interest_rate": _("Interest Rate"),
    # "simulation_year": _("Year of Simulation"),
}

scenario_field_order = [
    "project",
    "name",
    "evaluated_period",
    # "timeframe_choice",
    "time_step",
    "start_date",
    # "capex_fix",
    "interest_rate",
    # "simulation_year"
]


class ScenarioCreateForm(OpenPlanModelForm):
    field_order = scenario_field_order

    class Meta:
        model = Scenario
        exclude = ["id", "capex_var", "opex_fix", "opex_var"]
        widgets = scenario_widgets
        labels = scenario_labels

    def __init__(self, *args, **kwargs):
        project_queryset = kwargs.pop("project_queryset", None)
        super().__init__(*args, **kwargs)
        if project_queryset is not None:
            self.fields["project"].queryset = project_queryset
        else:
            self.fields["project"] = forms.ChoiceField(label="Project", choices=())
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class ScenarioSelectProjectForm(OpenPlanModelForm):
    field_order = scenario_field_order

    class Meta:
        model = Scenario
        fields = ["project"]
        widgets = scenario_widgets
        labels = scenario_labels

    def __init__(self, *args, **kwargs):
        project_queryset = kwargs.pop("project_queryset", None)
        super().__init__(*args, **kwargs)
        if project_queryset is not None:
            self.fields["project"].queryset = project_queryset
        else:
            self.fields["project"] = forms.ChoiceField(label="Project", choices=())
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class ScenarioUpdateForm(OpenPlanModelForm):
    field_order = scenario_field_order

    class Meta:
        model = Scenario
        exclude = ["id", "capex_var", "opex_fix", "opex_var"]
        widgets = scenario_widgets
        labels = scenario_labels

    def __init__(self, *args, **kwargs):
        project_queryset = kwargs.pop("project_queryset", None)
        super().__init__(*args, **kwargs)
        if project_queryset is not None:
            self.fields["project"].queryset = project_queryset
        else:
            self.fields["project"] = forms.ChoiceField(label="Project", choices=())

        # Deactivate Simulation Year and User Mode for changes
        # self.fields["simulation_year"].disabled = True
        # self.fields["user_mode_choice"].disabled = True

        # self.fields["simulation_year"].widget.attrs['readonly'] = 'readonly'
        # self.fields["user_mode_choice"].widget.attrs['readonly'] = 'readonly'

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = False  # don't include <form> tag


# endregion Scenario


class MinRenewableConstraintForm(OpenPlanModelForm):
    class Meta:
        model = MinRenewableConstraint
        exclude = ["scenario"]


class MaxEmissionConstraintForm(OpenPlanModelForm):
    class Meta:
        model = MaxEmissionConstraint
        exclude = ["scenario"]


class MinDOAConstraintForm(OpenPlanModelForm):
    class Meta:
        model = MinDOAConstraint
        exclude = ["scenario"]


class NZEConstraintForm(OpenPlanModelForm):
    class Meta:
        model = NZEConstraint
        exclude = ["scenario", "value"]


class SensitivityAnalysisForm(ModelForm):
    output_parameters_names = forms.MultipleChoiceField(
        choices=[
            (v, _(KPI_PARAMETERS_ASSETS[v]["verbose"])) for v in KPI_PARAMETERS_ASSETS
        ]
    )

    class Meta:
        model = SensitivityAnalysis
        fields = [
            "name",
            "variable_name",
            "variable_min",
            "variable_max",
            "variable_step",
            "variable_reference",
            "output_parameters_names",
        ]

    def __init__(self, *args, **kwargs):
        scen_id = kwargs.pop("scen_id", None)
        super().__init__(*args, **kwargs)

        forbidden_parameters_for_sa = ("name", "input_timeseries")

        if scen_id is not None:
            scenario = Scenario.objects.get(id=scen_id)
            asset_parameters = []
            for asset in scenario.asset_set.all():
                asset_parameters += [
                    (
                        f"{asset.name}.{p}",
                        _(parameters_helper.get_doc_verbose(p)) + f" ({asset.name})",
                    )
                    for p in asset.visible_fields
                    if p not in forbidden_parameters_for_sa
                ]
            self.fields["variable_name"] = forms.ChoiceField(choices=asset_parameters)
            # self.fields["output_parameters_names"] = forms.MultipleChoiceField(choices = [(v, _(KPI_PARAMETERS_ASSETS[v]["verbose"])) for v in KPI_PARAMETERS_ASSETS])
            # TODO restrict possible parameters here
            self.fields["output_parameters_names"].choices = [
                (v, _(KPI_PARAMETERS_ASSETS[v]["verbose"]))
                for v in KPI_PARAMETERS_ASSETS
            ]

    def clean_output_parameters_names(self):
        """method which gets called upon form validation"""
        data = self.cleaned_data["output_parameters_names"]
        data_js = json.dumps(data)
        return data_js


class COPCalculatorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["temperature_high"] = DualNumberField(
            default=60, min=-273, param_name="temperature_high"
        )
        self.fields["temperature_low"] = DualNumberField(
            default=40, min=-273, param_name="temperature_low"
        )

    class Meta:
        model = COPCalculator
        exclude = ["id", "scenario", "asset", "mode"]


class BusForm(OpenPlanModelForm):
    def __init__(self, *args, **kwargs):
        bus_type_name = kwargs.pop("asset_type", None)  # always = bus
        view_only = kwargs.pop("view_only", False)
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({f"df-{field}": ""})
            if view_only is True:
                self.fields[field].disabled = True

    class Meta:
        model = Bus
        fields = ["name", "type"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Bus Name",
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "type": forms.Select(
                choices=ENERGY_VECTOR,
                attrs={
                    "data-bs-toggle": "tooltip",
                    "title": _("The energy Vector of the connected assets."),
                    "style": "font-weight:400; font-size:13px;",
                },
            ),
        }
        labels = {"name": _("Name"), "type": _("Energy carrier")}


# class SuggestionForm(OpenPlanModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)


#     class Meta:
#         model = Asset
#         fields = ["capex", "opex", "lifetime"]
#         widgets = {
#             "capex": forms.NumberInput(
#                 attrs={
#                     "placeholder": "e.g. 4000",
#                     "min": "0.0",
#                     "step": ".01",
#                     "data-bs-toggle": "tooltip",
#                     "title": _(
#                         "Actual CAPEX of the asset, i.e., specific investment costs."
#                     ),
#                     "style": "font-weight:400; font-size:13px;",
#                 }
#             ),
#             "opex": forms.NumberInput(
#                 attrs={
#                     "placeholder": "e.g. 0",
#                     "min": "0.0",
#                     "step": ".01",
#                     "data-bs-toggle": "tooltip",
#                     "title": _(
#                         "Actual OPEX of the asset, i.e., specific operational and maintenance costs."
#                     ),
#                     "style": "font-weight:400; font-size:13px;",
#                 }
#             ),
#             "lifetime": forms.NumberInput(
#                 attrs={
#                     "placeholder": "e.g. 10 years",
#                     "min": "0",
#                     "step": "1",
#                     "data-bs-toggle": "tooltip",
#                     "title": _(
#                         "Number of operational years of the asset until it has to be replaced."
#                     ),
#                     "style": "font-weight:400; font-size:13px;",
#                 }
#             ),
#         }
class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class AssetCreateForm(OpenPlanModelForm):
    def __init__(self, *args, **kwargs):
        self.asset_type_name = kwargs.pop("asset_type", None)
        scenario_id = kwargs.pop("scenario_id", None)
        view_only = kwargs.pop("view_only", False)
        self.existing_asset = kwargs.get("instance", None)
        # get the connections with busses
        self.input_output_mapping = kwargs.pop("input_output_mapping", None)

        super().__init__(*args, **kwargs)
        # which fields exists in the form are decided upon AssetType saved in the db
        asset_type = AssetType.objects.get(asset_type=self.asset_type_name)
        [
            self.fields.pop(field)
            for field in list(self.fields)
            if field not in asset_type.visible_fields
        ]

        self.timestamps = None
        if self.existing_asset is not None:
            self.timestamps = self.existing_asset.timestamps
        elif scenario_id is not None:
            qs = Scenario.objects.filter(id=scenario_id)
            if qs.exists():
                self.timestamps = qs.get().get_timestamps()

        self.fields["inputs"] = forms.CharField(widget=forms.HiddenInput())

        if self.asset_type_name == "myTransformer":

            if self.existing_asset is None:

                self.fields["trafo_input_bus_1"] = UserModelChoiceField(
                    queryset=Bus.objects.all()
                )
                self.fields["trafo_input_bus_2"] = UserModelChoiceField(
                    queryset=Bus.objects.all()
                )
                self.fields["trafo_input_bus_3"] = UserModelChoiceField(
                    queryset=Bus.objects.all()
                )

                self.fields["trafo_output_bus_1"] = UserModelChoiceField(
                    queryset=Bus.objects.all()
                )
                self.fields["trafo_output_bus_2"] = UserModelChoiceField(
                    queryset=Bus.objects.all()
                )
                self.fields["trafo_output_bus_3"] = UserModelChoiceField(
                    queryset=Bus.objects.all()
                )

                self.fields["trafo_technicalp_bus_choice"] = UserModelChoiceField(
                    queryset=Bus.objects.all()
                )
                self.fields["trafo_invest_bus_choice"] = UserModelChoiceField(
                    queryset=Bus.objects.all()
                )
                self.fields["trafo_variableCosts_bus_choice"] = UserModelChoiceField(
                    queryset=Bus.objects.all()
                )
            for i in range(1, 4):
                self.fields["trafo_input_bus_" + str(i)].label = "Input bus " + str(i)
                self.fields["trafo_input_conversionf_" + str(i)].label = (
                    "Input conversion factor " + str(i)
                )

                self.fields["trafo_output_bus_" + str(i)].label = "Output bus " + str(i)
                self.fields["trafo_output_conversionf_" + str(i)].label = (
                    "Output conversion factor " + str(i)
                )
            self.fields["trafo_technicalp_bus_choice"].label = (
                "Bus the technical parameters refer to"
            )
            self.fields["trafo_invest_bus_choice"].label = (
                "Bus the invest modell refers to"
            )
            self.fields["trafo_variableCosts_bus_choice"].label = (
                "Bus the variable costs refer to"
            )

        if self.asset_type_name == "heat_pump":
            self.fields["efficiency"] = DualNumberField(
                default=1, min=1, param_name="efficiency"
            )
            self.fields["efficiency"].label = "COP"

        if self.asset_type_name == "chp":
            self.fields["efficiency"] = DualNumberField(
                default=1, min=0, max=1, param_name="efficiency"
            )
            self.fields["efficiency"].label = _(
                "Electrical efficiency with no heat extraction"
            )

            self.fields["efficiency"].help_text = (
                "This is the custom help text for chp efficiency"
            )

            self.fields["efficiency_multiple"] = DualNumberField(
                default=1, min=0, max=1, param_name="efficiency_multiple"
            )
            self.fields["efficiency_multiple"].label = _(
                "Thermal efficiency with maximal heat extraction"
            )

            self.fields["thermal_loss_rate"].label = _("Stromverlustkenzahl")

        if self.asset_type_name == "chp_fixed_ratio":

            self.fields["efficiency"].label = _("Efficiency gaz to electricity")

            # TODO
            self.fields["efficiency"].help_text = (
                "This is the custom help text for chp efficiency"
            )

            self.fields["efficiency_multiple"].widget = forms.NumberInput(
                attrs={
                    "placeholder": _("eg. 0.1"),
                    "min": 0.0,
                    "max": 1.0,
                    "step": "0.00001",
                }
            )
            self.fields["efficiency_multiple"].label = _("Efficiency gaz to heat")

        if "dso" in self.asset_type_name:

            self.fields["energy_price"] = DualNumberField(
                default=0.1, param_name="energy_price"
            )
            self.fields["feedin_tariff"] = DualNumberField(
                default=0.1, param_name="feedin_tariff"
            )

        """ DrawFlow specific configuration, add a special attribute to 
            every field in order for the framework to be able to export
            the data to json.
            !! This addition doesn't affect the previous behavior !!
        """
        for field in self.fields:
            if field == "renewable_asset" and self.asset_type_name in RENEWABLE_ASSETS:
                self.fields[field].initial = True
            self.fields[field].widget.attrs.update({f"df-{field}": ""})
            if field == "input_timeseries":
                self.fields[field].required = False  # self.is_input_timeseries_empty()
            if field == "choice_load_profile":
                self.fields[field].required = False
            # trafo for expert
            if field == "trafo_input_bus_2":
                self.fields[field].required = False
            if field == "trafo_input_bus_3":
                self.fields[field].required = False

            if field == "trafo_output_bus_2":
                self.fields[field].required = False
            if field == "trafo_output_bus_3":
                self.fields[field].required = False

            if field == "trafo_technicalp_bus_choice":
                self.fields[field].required = False
            if field == "trafo_invest_bus_choice":
                self.fields[field].required = False
            if field == "trafo_variableCosts_bus_choice":
                self.fields[field].required = False

            if view_only is True:
                self.fields[field].disabled = True
        """ ----------------------------------------------------- """

    def is_input_timeseries_empty(self):
        if self.existing_asset is not None:
            return self.existing_asset.is_input_timeseries_empty()
        else:
            return True

    def clean_input_timeseries(self):
        """Override built-in Form method which is called upon form validation"""
        try:
            input_timeseries_values = []
            timeseries_file = self.files.get("input_timeseries", None)
            # read the timeseries from file if any
            if timeseries_file is not None:
                input_timeseries_values = parse_input_timeseries(timeseries_file)
                # TODO here list the possible options
            else:
                # set the previous timeseries from the asset if any
                if self.is_input_timeseries_empty() is False:
                    input_timeseries_values = (
                        self.existing_asset.input_timeseries_values
                    )
            return input_timeseries_values
        except json.decoder.JSONDecodeError as ex:
            raise ValidationError(
                _(
                    "File not properly formatted. Please ensure you upload a comma separated array of values. E.g. [1,2,0.32]"
                )
            )
        except TypeError as e:
            raise ValidationError(str(e))
        except Exception as ex:
            raise ValidationError(_("Could not parse a file. Did you upload one?"))

    def clean_efficiency_multiple(self):
        data = self.cleaned_data["efficiency_multiple"]
        if self.asset_type_name == "chp_fixed_ratio":
            try:
                data = float(data)
            except ValueError:
                raise ValidationError("Please enter a float value between 0.0 and 1.0")
            if 0 <= data <= 1:
                pass
            else:
                raise ValidationError("Please enter a float value between 0.0 and 1.0")
            data = str(data)
        return data

    def clean(self):
        cleaned_data = super().clean()
        if "installed_capacity" in cleaned_data and "age_installed" in cleaned_data:
            if (
                cleaned_data["installed_capacity"] == 0.0
                and cleaned_data["age_installed"] > 0
            ):
                self.add_error(
                    "age_installed",
                    _(
                        "If you have no installed capacity, age installed should also be 0"
                    ),
                )

        if self.asset_type_name == "heat_pump":
            efficiency = cleaned_data["efficiency"]
            self.timeseries_same_as_timestamps(efficiency, "efficiency")

        if self.asset_type_name == "chp_fixed_ratio":
            if (
                float(cleaned_data["efficiency"])
                + float(cleaned_data["efficiency_multiple"])
                > 1
            ):
                msg = _("The sum of the efficiencies should not exceed 1")
                self.add_error("efficiency", msg)
                self.add_error("efficiency_multiple", msg)

        if "dso" in self.asset_type_name:
            feedin_tariff = np.array([cleaned_data["feedin_tariff"]])
            energy_price = np.array([cleaned_data["energy_price"]])
            diff = feedin_tariff - energy_price
            max_capacity = cleaned_data.get("max_capacity", 0)
            if (diff > 0).any() is True and max_capacity == 0:
                msg = _(
                    "Feed-in tariff > energy price for some of simulation's timesteps. This would cause an unbound solution and terminate the optimization. Please reconsider your feed-in tariff and energy price."
                )
                self.add_error("feedin_tariff", msg)
            self.timeseries_same_as_timestamps(feedin_tariff, "feedin_tariff")
            self.timeseries_same_as_timestamps(energy_price, "energy_price")

        return cleaned_data

    def timeseries_same_as_timestamps(self, ts, param):
        if isinstance(ts, np.ndarray):
            ts = np.squeeze(ts).tolist()
        if isinstance(ts, float) is False and isinstance(ts, int) is False:
            if len(ts) > 1:
                if self.timestamps is not None:
                    if len(ts) != len(self.timestamps):
                        # TODO look for verbose of param
                        msg = (
                            _("The number of values of the parameter ")
                            + _(param)
                            + f" ({len(ts)})"
                            + _(" are not equal to the number of simulation timesteps")
                            + f" ({len(self.timestamps)})"
                            + _(
                                ". You can change the number of timesteps in the first step of scenario creation."
                            )
                        )
                        self.add_error(param, msg)

    class Meta:
        model = Asset
        exclude = ["scenario"]
        unit = "MW"
        widgets = {
            "optimize_cap": forms.Select(
                choices=BOOL_CHOICES,
                attrs={
                    "data-bs-toggle": "tooltip",
                    "title": _(
                        "True if the user wants to perform capacity optimization for various components as part of the simulation."
                    ),
                    "style": "font-weight:400; font-size:13px;",
                },
            ),
            "dispatchable": forms.Select(choices=TRUE_FALSE_CHOICES),
            "renewable_asset": forms.Select(
                choices=TRUE_FALSE_CHOICES,
                attrs={
                    "data-bs-toggle": "tooltip",
                    "title": _("Indicate if the asset is renewable or not."),
                    "style": "font-weight:400; font-size:13px;",
                },
            ),
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Asset Name",
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "capex_fix": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 10000",
                    "min": "0.0",
                    "step": ".01",
                    "data-bs-toggle": "tooltip",
                    "title": _(
                        " A fixed cost to implement the asset, eg. planning costs which do not depend on the (optimized) asset capacity."
                    ),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "capex_var": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 4000",
                    "min": "0.0",
                    "step": ".01",
                    "data-bs-toggle": "tooltip",
                    "title": _(
                        " Actual CAPEX of the asset, i.e., specific investment costs."
                    ),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "opex_fix": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 0",
                    "min": "0.0",
                    "step": ".01",
                    "data-bs-toggle": "tooltip",
                    "title": _(
                        "Actual OPEX of the asset, i.e., specific operational and maintenance costs."
                    ),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "opex_var": forms.NumberInput(
                attrs={
                    "placeholder": "Currency",
                    "min": "0.0",
                    "step": ".01",
                    "data-bs-toggle": "tooltip",
                    "title": _(
                        "Variable cost associated with a flow through/from the asset."
                    ),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            # "lifetime": forms.NumberInput(
            #     attrs={
            #         "placeholder": "e.g. 10 years",
            #         "min": "0",
            #         "step": "1",
            #         "data-bs-toggle": "tooltip",
            #         "title": _(
            #             "Number of operational years of the asset until it has to be replaced."
            #         ),
            #         "style": "font-weight:400; font-size:13px;",
            #     }
            # ),
            # # TODO: Try changing this to FileInput
            # "input_timeseries": forms.FileInput(
            #     attrs={
            #         "onchange": "plot_file_trace(obj=this.files, plot_id='timeseries_trace')"
            #     }
            # ),
            # 'input_timeseries': forms.Textarea(attrs={'placeholder': 'e.g. [4,3,2,5,3,...]',
            #                                           'style': 'font-weight:400; font-size:13px;'}),
            "crate": forms.NumberInput(
                attrs={
                    "placeholder": "factor of total capacity (kWh), e.g. 0.7",
                    "min": "0.0",
                    "max": "1.0",
                    "step": ".0001",
                    "data-bs-toggle": "tooltip",
                    "title": _(
                        "C-rate is the rate at which the storage can charge or discharge relative to the nominal capacity of the storage. A c-rate of 1 implies that the battery can discharge or charge completely in a single timestep."
                    ),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "efficiency": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 0.99",
                    "data-bs-toggle": "tooltip",
                    "title": _("Ratio of energy output/energy input."),
                    "style": "font-weight:400; font-size:13px;",
                    "min": "0.0",
                    # "max": "1.0",
                    "step": ".01",
                }
            ),
            "soc_max": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 0.95",
                    "min": "0.0",
                    "max": "1.0",
                    "step": ".01",
                    "data-bs-toggle": "tooltip",
                    "title": _(
                        "The maximum permissible level of charge in the battery (generally, it is when the battery is filled to its nominal capacity), represented by the value 1.0. Users can  also specify a certain value as a factor of the actual capacity."
                    ),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "soc_min": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 0.1",
                    "min": "0.0",
                    "max": "1.0",
                    "step": ".01",
                    "data-bs-toggle": "tooltip",
                    "title": _(
                        "The minimum permissible level of charge in the battery as a factor of the nominal capacity of the battery."
                    ),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "maximum_capacity": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 1000",
                    "min": "0.0",
                    "step": ".01",
                    "data-bs-toggle": "tooltip",
                    "title": _("The maximum installable capacity."),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "energy_price": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 0.1",
                    "min": "0.0",
                    "step": ".0001",
                    "data-bs-toggle": "tooltip",
                    "title": _("Price of electricity sourced from the utility grid."),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "feedin_tariff": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 0.0",
                    "min": "0.0",
                    "step": ".0001",
                    "data-bs-toggle": "tooltip",
                    "title": _("Price received for feeding electricity into the grid."),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "feedin_cap": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 0.0",
                    "min": "0.0",
                    "data-bs-toggle": "tooltip",
                    "title": _("Capping the feedin capacity of a DSO."),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "peak_demand_pricing": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 60",
                    "min": "0.0",
                    "step": ".01",
                    "data-bs-toggle": "tooltip",
                    "title": _(
                        "Price to be paid additionally for energy-consumption based on the peak demand of a period."
                    ),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "peak_demand_pricing_period": forms.NumberInput(
                attrs={
                    "placeholder": "times per year, e.g. 2",
                    "data-bs-toggle": "tooltip",
                    "title": _(
                        "Number of reference periods in one year for the peak demand pricing. Only one of the following are acceptable values: 1 (yearly), 2, 3 ,4, 6, 12 (monthly)."
                    ),
                    "style": "font-weight:400; font-size:13px;",
                    "min": "1",
                    "max": "12",
                    "step": "1",
                }
            ),
            "renewable_share": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 0.1",
                    "min": "0.0",
                    "max": "1.0",
                    "step": ".0001",
                    "data-bs-toggle": "tooltip",
                    "title": "The share of renewables in the generation mix of the energy supplied by the DSO (utility).",
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "installed_capacity": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 50",
                    "min": "0.0",
                    "step": ".01",
                    "data-bs-toggle": "tooltip",
                    "title": _(
                        "The already existing installed capacity in-place, which will also be replaced after its lifetime."
                    ),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "age_installed": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 10",
                    "min": "0.0",
                    "step": "1",
                    "data-bs-toggle": "tooltip",
                    "title": _(
                        "The number of years the asset has already been in operation."
                    ),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            #########################################################################
            "variable_costs": forms.NumberInput(
                attrs={
                    "placeholder": "e. g. 50 €/" + unit + "h",
                    "min": "0.0",
                    "step": ".01",
                    "data-bs-toggle": "tooltip",
                    "title": _(
                        "Variable cost associated with a flow through/from the asset."
                    ),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "nominal_value": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 50 " + unit,
                    "min": "0.0",
                    "step": ".01",
                    "data-bs-toggle": "tooltip",
                    "title": _("The already existing installed capacity in-place"),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "_min": forms.NumberInput(
                attrs={
                    "placeholder": "factor of energy flow (" + unit + "h) e.g. 0.7",
                    "min": "0.0",
                    "max": "1.0",
                    "step": ".0001",
                    "data-bs-toggle": "tooltip",
                    "title": _("Nominal minimum value of the flow"),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "_max": forms.NumberInput(
                attrs={
                    "placeholder": "factor of energy flow (" + unit + "h) e.g. 0.7",
                    "min": "0.0",
                    "max": "1.0",
                    "step": ".0001",
                    "data-bs-toggle": "tooltip",
                    "title": _("Normed maximum value of the flow"),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "nonconvex": forms.Select(
                choices=TRUE_FALSE_CHOICES,
                attrs={
                    "data-bs-toggle": "tooltip",
                    "title": _(
                        "If a nonconvex flow object is added here, the flow constraints will be altered significantly as the mathematical model for the flow will be different"
                    ),
                    "style": "font-weight:400; font-size:13px;",
                },
            ),
            "summed_max": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 1000 " + unit + "h",
                    "min": "0.0",
                    "step": ".01",
                    "data-bs-toggle": "tooltip",
                    "title": _(
                        "Specific maximum value summed over all timesteps. Will be multiplied with the nominal_value to get the absolute limit."
                    ),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "summed_min": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 1000 " + unit + "h",
                    "min": "0.0",
                    "step": ".01",
                    "data-bs-toggle": "tooltip",
                    "title": _(
                        "Specific minimum value summed over all timesteps. Will be multiplied with the nominal_value to get the absolute limit."
                    ),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "lifetime": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 10 years",
                    "min": "0",
                    "step": "1",
                    "data-bs-toggle": "tooltip",
                    "title": _(
                        "Number of operational years of the asset until it has to be replaced."
                    ),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            # TODO: Try changing this to FileInput
            "input_timeseries": forms.FileInput(
                attrs={
                    "required": False,
                    "onchange": "plot_file_trace(obj=this.files, plot_id='timeseries_trace')",
                }
            ),
            "annual_energy_consumption": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 5000 " + unit + "h",
                    "min": "0.0",
                    "step": ".01",
                    "data-bs-toggle": "tooltip",
                    "title": _("Your yearly energy consumption."),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "choice_load_profile": forms.Select(
                attrs={
                    "required": False,
                    "onchange": "makePlotlyLoadProfile(this.value)",
                }
            ),
            "capex": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 50000 €/"
                    + unit
                    + " resp. €/"
                    + unit
                    + "h for storage",
                    "min": "0.0",
                    "step": ".01",
                    "data-bs-toggle": "tooltip",
                    "title": _(
                        "Actual CAPEX of the asset, i.e., specific investment costs."
                    ),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "opex": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 5% of CAPEX",
                    "min": "0.0",
                    "step": ".01",
                    "data-bs-toggle": "tooltip",
                    "title": _(
                        "Actual OPEX of the asset, i.e., specific operational and maintenance costs."
                    ),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "offset": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 10000 €",
                    "min": "0.0",
                    "step": ".01",
                    "data-bs-toggle": "tooltip",
                    "title": _(
                        " A fixed cost to implement the asset, eg. planning costs which do not depend on the (optimized) asset capacity."
                    ),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "maximum": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 100 "
                    + unit
                    + " resp. "
                    + unit
                    + "h for storage",
                    "min": "0.0",
                    "step": ".01",
                    "data-bs-toggle": "tooltip",
                    "title": _("Maximum of the additional invested capacity/power."),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "minimum": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 100 "
                    + unit
                    + " resp. "
                    + unit
                    + "h for storage",
                    "min": "0.0",
                    "step": ".01",
                    "data-bs-toggle": "tooltip",
                    "title": _("Minimum of the additional invested capacity/power."),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "existing": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 100 "
                    + unit
                    + " resp. "
                    + unit
                    + "h for storage",
                    "min": "0.0",
                    "step": ".01",
                    "data-bs-toggle": "tooltip",
                    "title": _("Existing / installed capacity."),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "balanced": forms.Select(
                choices=TRUE_FALSE_CHOICES,
                attrs={
                    "data-bs-toggle": "tooltip",
                    "title": _(""),
                    "style": "font-weight:400; font-size:13px;",
                },
            ),
            "nominal_storage_capacity": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 100 " + unit + "h",
                    "min": "0.0",
                    "step": ".01",
                    "data-bs-toggle": "tooltip",
                    "title": _("Installed storage capacity."),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "inflow_conversion_factor": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 0.99",
                    "data-bs-toggle": "tooltip",
                    "title": _("Ratio of energy output/energy input."),
                    "style": "font-weight:400; font-size:13px;",
                    "min": "0.0",
                    "max": "1.0",
                    "step": ".01",
                }
            ),
            "outflow_conversion_factor": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 0.99",
                    "data-bs-toggle": "tooltip",
                    "title": _("Ratio of energy output/energy input."),
                    "style": "font-weight:400; font-size:13px;",
                    "min": "0.0",
                    "max": "1.0",
                    "step": ".01",
                }
            ),
            "invest_relation_input_capacity": forms.NumberInput(
                attrs={
                    "placeholder": "factor of total capacity (" + unit + "h), e.g. 0.7",
                    "min": "0.0",
                    "max": "1.0",
                    "step": ".0001",
                    "data-bs-toggle": "tooltip",
                    "title": _(
                        "C-rate is the rate at which the storage can charge or discharge relative to the nominal capacity of the storage. A c-rate of 1 implies that the battery can discharge or charge completely in a single timestep."
                    ),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "invest_relation_output_capacity": forms.NumberInput(
                attrs={
                    "placeholder": "factor of total capacity (" + unit + "h), e.g. 0.7",
                    "min": "0.0",
                    "max": "1.0",
                    "step": ".0001",
                    "data-bs-toggle": "tooltip",
                    "title": _(
                        "C-rate is the rate at which the storage can charge or discharge relative to the nominal capacity of the storage. A c-rate of 1 implies that the battery can discharge or charge completely in a single timestep."
                    ),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "initial_storage_level": forms.NumberInput(
                attrs={
                    "placeholder": "factor of total capacity ("
                    + unit
                    + "h), e.g. 0.5 means half full",
                    "min": "0.0",
                    "max": "1.0",
                    "step": ".01",
                    "data-bs-toggle": "tooltip",
                    "title": _(""),
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "eco_params_flow_choice": forms.Select(
                choices=FLOW_CHOICE,
                attrs={
                    "data-bs-toggle": "tooltip",
                    "title": _(
                        "This parameter specifies whether the economic parameters should refer to the transformer input or the transformer output."
                    ),
                    "style": "font-weight:400; font-size:13px;",
                },
            ),
            "tec_params_flow_choice": forms.Select(
                choices=FLOW_CHOICE,
                attrs={
                    "data-bs-toggle": "tooltip",
                    "title": _(
                        "This parameter specifies whether the technical parameters should refer to the transformer input or the transformer output."
                    ),
                    "style": "font-weight:400; font-size:13px;",
                },
            ),
            "emission_factor": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 0.201 in t_CO2/" + unit + "h",
                    "min": "0.0",
                    "max": "1.0",
                    "step": ".0001",
                    "data-bs-toggle": "tooltip",
                    "title": "",
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "renewable_factor": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 1",
                    "min": "0.0",
                    "max": "1.0",
                    "step": ".0001",
                    "data-bs-toggle": "tooltip",
                    "title": "This parameter enters into the condition 'Bilanziell Erneuerbar' and is multiplied by the amount of energy of the respective component.",
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "oep_table_name": forms.TextInput(
                attrs={
                    "placeholder": "e.g. electricity_load_sample",
                    "data-bs-toggle": "tooltip",
                    "title": "This parameter specifies the Open Energy Platform table from the model draft to be used.",
                    "style": "font-weight:400; font-size:13px;",
                }
            ),
            "oep_column_name": forms.TextInput(
                attrs={
                    "placeholder": "e.g. electricity_load",
                    "data-bs-toggle": "tooltip",
                    "title": "This parameter specifies the column of the OEP table to be used.",
                    "style": "font-weight:400; font-size:13px;",
                    # "required": False,
                    # "onchange": "makePlotlyLoadProfile(this.value)",
                }
            ),
            "source_choice": forms.Select(
                choices=SOURCE_CHOICE,
                attrs={
                    "data-bs-toggle": "tooltip",
                    "title": _(""),
                    "style": "font-weight:400; font-size:13px;",
                    "onchange": "loadPredefindedDataKindofSource(this.value)",
                },
            ),
            # "year_choice_source": forms.Select(
            #     choices=YEAR_CHOICE,
            #     attrs={
            #         "data-bs-toggle": "tooltip",
            #         "title": _(""),
            #         "style": "font-weight:400; font-size:13px;",
            #         "onchange": "PredefindedSourceYear(this.value)",
            #     },
            # ),
            # "year_choice_trafo": forms.Select(
            #     choices=YEAR_CHOICE,
            #     attrs={
            #         "data-bs-toggle": "tooltip",
            #         "title": _(""),
            #         "style": "font-weight:400; font-size:13px;",
            #         "onchange": "PredefindedTrafoYear(this.value)",
            #     },
            # ),
            "trafo_choice": forms.Select(
                choices=TRAFO_CHOICE,
                attrs={
                    "data-bs-toggle": "tooltip",
                    "title": _(""),
                    "style": "font-weight:400; font-size:13px;",
                    "onchange": "loadPredefindedDataKindofTrafo(this.value)",
                },
            ),
            "efficiency_el": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 0.45",
                    "data-bs-toggle": "tooltip",
                    "title": _("Ratio of energy output/energy input."),
                    "style": "font-weight:400; font-size:13px;",
                    "min": "0.0",
                    "max": "1.0",
                    "step": ".01",
                }
            ),
            "efficiency_th": forms.NumberInput(
                attrs={
                    "placeholder": "e.g. 0.43",
                    "data-bs-toggle": "tooltip",
                    "title": _("Ratio of energy output/energy input."),
                    "style": "font-weight:400; font-size:13px;",
                    "min": "0.0",
                    "max": "1.0",
                    "step": ".01",
                }
            ),
            # "year_choice_storage": forms.Select(
            #     choices=YEAR_CHOICE,
            #     attrs={
            #         "data-bs-toggle": "tooltip",
            #         "title": _(""),
            #         "style": "font-weight:400; font-size:13px;",
            #         "onchange": "PredefindedStorageYear(this.value)",
            #     },
            # ),
            "storage_choice": forms.Select(
                choices=STORAGE_CHOICE,
                attrs={
                    "data-bs-toggle": "tooltip",
                    "title": _(""),
                    "style": "font-weight:400; font-size:13px;",
                    "onchange": "loadPredefindedDataKindofStorage(this.value)",
                },
            ),
            "trafo_input_output_variation_choice": forms.Select(
                choices=TRAFO_I_O_VARIATION_CHOICE,
                attrs={
                    "data-bs-toggle": "tooltip",
                    "title": _(""),
                    "style": "font-weight:400; font-size:13px;",
                    "onchange": "get_trafo_variation(this.value)",
                },
            ),
        }
        labels = {
            "input_timeseries": _("Timeseries vector"),
            "oep_table_name": _("OEP table name in Model draft"),
        }
        help_texts = {
            "input_timeseries": _(
                "You can upload your timeseries as xls(x), csv or json format. Either there is one column with the values of the timeseries matching the scenario timesteps, or there are two columns, the first one being the timestamps and the second one the values of the timeseries. If you upload a spreadsheet with more than one tab only the first tab will be considered. The timeseries in csv format is expected to be in comma separated values with dot as decimal separator."
            )
        }


class StorageForm(AssetCreateForm):
    def __init__(self, *args, **kwargs):
        asset_type_name = kwargs.pop("asset_type", None)
        super(StorageForm, self).__init__(*args, asset_type="capacity", **kwargs)
        self.fields["dispatchable"].widget = forms.HiddenInput()
        self.fields["dispatchable"].initial = True
        self.fields["installed_capacity"].label = _("Installed capacity (kWh)")
        if asset_type_name != "hess":
            self.fields["fixed_thermal_losses_relative"].widget = forms.HiddenInput()
            self.fields["fixed_thermal_losses_relative"].initial = 0
            self.fields["fixed_thermal_losses_absolute"].widget = forms.HiddenInput()
            self.fields["fixed_thermal_losses_absolute"].initial = 0
            self.fields["thermal_loss_rate"].widget = forms.HiddenInput()
            self.fields["thermal_loss_rate"].initial = 0
        else:
            self.fields["fixed_thermal_losses_relative"] = DualNumberField(
                default=0.1, min=0, max=1, param_name="fixed_thermal_losses_relative"
            )
            self.fields["fixed_thermal_losses_absolute"] = DualNumberField(
                default=0.1, min=0, param_name="fixed_thermal_losses_absolute"
            )

    field_order = [
        "name",
        "capex_fix",
        "capex_var",
        "opex_fix",
        "opex_var",
        "installed_capacity",
        "optimize_cap",
        "lifetime",
        "age_installed",
        "crate",
        "efficiency",
        "soc_max",
        "soc_min",
        "dispatchable",
    ]


class StorageForm_II(AssetCreateForm):
    def __init__(self, *args, **kwargs):
        asset_type_name = kwargs.pop("asset_type", None)
        super(StorageForm_II, self).__init__(
            *args, asset_type=asset_type_name, **kwargs
        )
        # self.fields["dispatchable"].widget = forms.HiddenInput()
        # self.fields["dispatchable"].initial = True
        # self.fields["installed_capacity"].label = _("Installed capacity (kWh)")
        self.fields["thermal_loss_rate"].widget = forms.NumberInput(
            attrs={
                "placeholder": _("eg. 0.1"),
                "min": 0.0,
                "max": 1.0,
                "step": "0.00001",
                "style": "font-weight:400; font-size:13px;",
            }
        )
        self.fields["fixed_thermal_losses_relative"].widget = forms.NumberInput(
            attrs={
                "placeholder": _("eg. 0.1"),
                "min": 0.0,
                "max": 1.0,
                "step": "0.00001",
                "style": "font-weight:400; font-size:13px;",
            }
        )
        self.fields["fixed_thermal_losses_absolute"].widget = forms.NumberInput(
            attrs={
                "placeholder": _("eg. 0.1"),
                "min": 0.0,
                "max": 1.0,
                "step": "0.00001",
                "style": "font-weight:400; font-size:13px;",
            }
        )
