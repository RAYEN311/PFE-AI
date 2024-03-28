from detecto.core import Model
from detecto import utils, visualize

labels = ['PCB-MODEL-0', 'normal-spring_finger', 'defected-spring_finger','normal-through','defected-through']

model = Model.load('./pcb_detect.pth' , labels )



image1 = utils.read_image('./datasets/images/validation/1710111756965.jpg')

images = [image1]

visualize.plot_prediction_grid(model,images, score_filter= 0.3 )
#visualize.detect_live(model , 0.8) 