from channels.layers import get_channel_layer, BaseChannelLayer


def check_and_get_channel_layer() -> BaseChannelLayer:
    channel_layer = get_channel_layer()
    if channel_layer is None:
        raise RuntimeError("Channel layer is not configured.")
    return channel_layer