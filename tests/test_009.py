# https://www.terraform.io/docs/configuration/locals.html

import terrascript
import terrascript.provider
import terrascript.data

from shared import assert_equals_json


def test():
    """Update method (009)"""

    # First terrascript
    config = terrascript.Terrascript()
    config.add(terrascript.Variable('access_key', default=''))
    config.add(terrascript.provider.aws(region='us-east-1'))

    config.add(terrascript.data.aws_ami('example', most_recent=True, owners=['self'],
                                        tags=dict(Name="app-server", Tested="true")))

    # Second terrascript
    ts2 = terrascript.Terrascript()
    ts2.add(terrascript.Variable('secret_key', default=''))
    ts2.add(terrascript.provider.aws(region='us-east-2', alias='useast2'))
    ts2.add(terrascript.data.aws_ami('example2', most_recent=True, owners=['self'],
                                     tags=dict(Name="app-server", Tested="true")))
    # Replace first aws_ami
    ts2.add(terrascript.data.aws_ami('example', most_recent=True, owners=['self'],
                                     tags=dict(Name="app-server2", Tested="true")))

    config.merge(ts2)  # ts1 is now merged with ts2 items
    print(config)
    assert_equals_json(config, 'test_009.tf.json')
