import rospkg

__all__ = [
    "get_ros_package_path",
]


def get_ros_package_path(package_name):
    """ Returns the path to a package. """

    rospack = rospkg.RosPack()
    return rospack.get_path(package_name)

# def display_filename(filename):
#     """ Displays a filename in a possibly simpler way """
#     return friendly_path(filename)
