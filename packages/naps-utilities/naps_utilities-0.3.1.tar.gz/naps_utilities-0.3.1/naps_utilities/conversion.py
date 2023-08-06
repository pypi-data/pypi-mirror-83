#Nécessaire pour la conversion vers/depuis ROS2
from builtin_interfaces.msg import Time
from sensor_msgs.msg import PointCloud2
from sensor_msgs.msg import PointField
from std_msgs.msg import Header

from array import array

  def to_ros_header(header_data):
      return Header(stamp=Time(
          sec=header_data['time']['sec'],
          nanosec=header_data['time']['nanosec']),
               frame_id=header_data['frame_id'])

  def to_ros_pointfields(pointfields_data):
      return [PointField(name=field['name'],
                    offset=field['offset'],
                    datatype=field['datatype'],
                    count=field['count']) for field in pointfields_data]

  def to_ros_PointCloud2(pc):
      msg = PointCloud2()
      #Données conservées "telles quelles"

      msg.height = pc.metadata['height']
      msg.width = pc.metadata['width']

      msg.is_bigendian = pc.metadata['is_bigendian']
      msg.point_step = pc.metadata['point_step']
      msg.row_step = pc.metadata['row_step']

      msg.is_dense = pc.metadata['is_dense']
      msg.header = to_header(pc.metadata['header'])
      msg.fields = to_pointfields(pc.metadata['fields'])

      if pc.metadata['keep_ring']:
          msg.data = array('B', np.concatenate(
              (pc.points.view(dtype=np.uint8),
               pc.rings.reshape((pc.metadata['nb_points'], -1)).view(dtype=np.uint8)),
              axis=1).ravel().tolist())

        else:
            msg.data = array('B', self.points.view(dtype=np.uint8).ravel().tolist())
        return msg
