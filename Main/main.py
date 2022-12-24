from kuberntesOperations import kubeOps
from colorama import Fore,Style

kube = kubeOps()

def printOpts():
    print(Fore.CYAN+"Menu of actions:")
    print("1. List all Pods")
    print("2. Describe a Pod of choice")
    print("3. Create a deployment for nginx:1.22.1 / busybox:1.34.1 ")
    print("4. Scale the number of pods created from previous deployments")
    print("5. Perform a rolling update on the pods from a deployment")
    print("6.Create a pod on every worker node (specify type of the node")
    print("7. Run the predefined scenario")
    print("Enter quit to Exit the program")
    print(Style.RESET_ALL)

choice="quit"
while(choice!="quite"):
    printOpts()
    choice=input("Enter your choice: ")
    if(choice=="1"):
        kube.listAllPods()
    elif(choice=="2"):
        kube.describePod("")
    elif(choice=="3"):
        kube.createDeployMent()
    elif(choice=="4"):
        kube.scaleDeployment()
    elif(choice=="5"):
        kube.perFormRollingUpdate()
    elif(choice=="6"):
        kube.createPodOnEachNode()
    elif(choice=="7"):
        kube.runPredefinedScenario()
    elif(choice=="quit"):
        print("Exiting the program")
        kube.ssh.close()
        break
    else:
        print("Invalid choice, please enter a valid choice")

