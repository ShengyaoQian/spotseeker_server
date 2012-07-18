from django.contrib import admin
from django.conf import settings
from django.utils.importlib import import_module
from spotseeker_server.models import *
from spotseeker_server.org_forms.uw_spot import ExtendedInfoForm


class SpotAdmin(admin.ModelAdmin):
    """ The admin model for a Spot.
    The ETag is excluded because it is generated on Spot save.
    """
    list_display = ("name",
                    "building_name",
                    "floor",
                    "room_number",
                    "capacity",
                    "organization",
                    "manager")
    list_filter = ["spottypes",
                   "building_name",
                   "organization",
                   "manager"]
    exclude = ('etag',)
admin.site.register(Spot, SpotAdmin)


class SpotImageAdmin(admin.ModelAdmin):
    """ The admin model for a SpotImage.
    Content-type, width, height, and ETag are all filled in by the server on
    SpotImage save.
    """
    exclude = ('content_type', 'width', 'height', 'etag',)
    list_filter = ["spot"]
admin.site.register(SpotImage, SpotImageAdmin)


class SpotAvailableHoursAdmin(admin.ModelAdmin):
    """ The admin model for SpotAvailableHours.
    """
    list_filter = ('day', 'spot')
admin.site.register(SpotAvailableHours, SpotAvailableHoursAdmin)


class SpotExtendedInfoAdmin(admin.ModelAdmin):
    """ The admin model for SpotExtendedInfo.
    """
    if hasattr(settings, 'SPOTSEEKER_SPOT_FORM'):
        module, attr = settings.SPOTSEEKER_SPOT_FORM.rsplit('.', 1)
        try:
            mod = import_module(module)
        except ImportError, e:
            raise ImproperlyConfigured('Error import module %s: "%s"' %
                                       (module, e))
        try:
            FormModule = getattr(mod, 'ExtendedInfoForm')
        except AttributeError:
            raise ImproperlyConfigured('Module "%s" does not define a ExtendedInfoForm class.' % (module, attr))
        form = FormModule
    list_display = ("spot", "key", "value")
    list_editable = ["key", "value"]
    list_filter = ["key", "spot"]
admin.site.register(SpotExtendedInfo, SpotExtendedInfoAdmin)


admin.site.register(SpotType)
admin.site.register(TrustedOAuthClient)
