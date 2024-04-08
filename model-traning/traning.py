from detecto.core import Model, Dataset

dataset = Dataset('./datasets/images/train')

model = Model(['PCB-MODEL-0', 'normal-spring_finger', 'defected-spring_finger','normal-through','defected-through'])

model.fit(dataset)

model.save('pcb_detect.pth')




#classes
# PCB-MODEL-0
# normal-spring_finger
# defected-spring_finger
# normal-through
# defected-through