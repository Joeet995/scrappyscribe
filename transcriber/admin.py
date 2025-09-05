from django.contrib import admin
from .models import AudioFile
from django.utils.html import format_html
from django.urls import reverse


class AudioFileAdmin(admin.ModelAdmin):
    # 1. First, define the method that generates the link.
    def view_detail_link(self, obj):
        """
        Creates a link to the custom detail page for this AudioFile.
        """
        # Check if the object has a primary key (it's saved to the DB)
        if obj.pk:
            # Build the URL for the detail page. 'transcriber' is the app namespace.
            url = reverse('transcriber:audiofile_detail', args=[obj.pk])
            # Return the HTML for the link
            return format_html('<a class="button" href="{}">View & Annotate</a>', url)
        return "-"  # Display a dash for unsaved objects

    # 2. Set a short, readable name for the admin list column header.
    view_detail_link.short_description = 'Action'

    # 3. NOW, define list_display and include the method name.
    # This tells the admin to call the `view_detail_link` method for each object.
    list_display = ('original_filename', 'status', 'uploaded_at', 'view_detail_link')
    
    # 4. (Optional) Make these fields read-only when editing in the admin
    readonly_fields = ('original_filename', 'uploaded_at')

# Finally, register the model with our CUSTOM admin class (AudioFileAdmin)
admin.site.register(AudioFile, AudioFileAdmin)