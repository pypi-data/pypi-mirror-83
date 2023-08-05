# import libs
from wasabi import Printer

# start the sister class
class sister():

    # define class structure
    def __init__(self, name=None):

        # object slots
        self.name = name

        # check if name was given
        if self.name is None:

            # set name to default
            self.name = "Sister"

        # initialize Printer
        msg = Printer()

        # print heading
        msg.divider(str("Welcome " + self.name))

        # create info section
        info_section = """

Congrats to becoming a sister. Being a sister is amazing and sometimes can be
hard. However, you are one of the most important people in your sibling's life.
So be there for your little baby sibling and have fun.

To start the advice section, you can just run the advice() method and I will 
guide you, hoping that you can please your little wonder.

Cheers and keep it up.

        """

         # print info
        print (info_section)

    # define advice function
    def get_advice(self):

        # initialize Printer
        msg = Printer()

        # print info message
        msg.info("Okay, " + self.name + " keep calm, I will guide you")

        # check the sex of the baby
        sex = input("Are you searching for adivce on a boy or a girl? ")

        # check if fed properly
        fed = input(str("Was your " + sex + 
                        " fed properly in the last 2 hours? (yes/no) "))

        # evaluate if baby is maybe hungry
        if fed=="no":
            
            # suggest trying to feed the baby
            msg.warn("Maybe your " + sex + " is hungry, try some nice food!")

            # break out of function
            return None

        # check if slept properly
        slept = input(str("Has your " + sex +
                          " slept properly in the last 1.5 hours? (yes/no) "))

        # evaluate if baby is maybe tired
        if slept=="no":

            # suggest trying to put the baby to sleep
            msg.warn("Maybe your " + sex + " is tired and wants to sleep!")

            # break out of function
            return None    

        # check if baby is maybe bored
        entertained = input(str("Is your " + sex + 
                                " active and wants to interact? (yes/no)"))
        
        # evaluate if baby might be bored
        if entertained=="yes":

            # suggest to talk to the baby
            msg.warn("Maybe your " + sex +
                     " is bored and you could sit down and have a chat.")

            # break out of function
            return None

        # if nothing detected so far, give advice
        msg.info(str("Your little " + sex +
                " neither hungry, nor tired, nor bored, just cuddle!"))