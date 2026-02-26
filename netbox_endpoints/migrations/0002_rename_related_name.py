"""Rename connected_interface related_name to avoid clash with NetBox core.

NetBox's Interface model has a built-in `connected_endpoints` property used by
the cable tracing / serialization system. Our ForeignKey's related_name
shadowed it, causing TypeError on device deletion.
"""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("netbox_endpoints", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="endpoint",
            name="connected_interface",
            field=models.ForeignKey(
                blank=True,
                help_text="Switch port this endpoint is connected to (for wired endpoints)",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="endpoint_connections",
                to="dcim.interface",
            ),
        ),
    ]
