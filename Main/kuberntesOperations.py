import paramiko
import pprint
from colorama import Fore, Style
import configparser

class kubeOps:
    def __init__(self):
        self.ssh = paramiko.SSHClient()
        self.config = configparser.ConfigParser()
        self.config.read("/home/cptblackbeard/Programes/python/kubernetes/Main/config.ini")
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect('3.110.219.249', username='ubuntu', password='', key_filename='cptblackbeardsEC2Instance.pem')
        print(Fore.GREEN+"****************** Connection Established  ******************")
        print(Fore.GREEN+"****************** Starting Docker and kubectl  ******************")
        print(Style.RESET_ALL)
        stdin,stdout, stderr = self.ssh.exec_command('ls -a')
        self.showSSHOutput(stdout.readline)
        


    def showSSHOutput(self, input):
        if(input!=[]):
            print(input)
        else:
            pass

    def showSSHOutPutLongRunningCommand(self,input):
        for line in iter(input.readline, ""):
            print(line, end="")
      

    def listAllPods(self):
        stdin,stdout, stderr = self.ssh.exec_command('kubectl get pods -o wide')
        self.showSSHOutPutLongRunningCommand(stdout)

    def describePod(self,podName):
        self.listAllPods()
        try:
            if(podName ==""):
                podName=input("Enter the name of the pod you want to describe: ")
                command="kubectl describe pod "+podName
                stdin,stdout, stderr = self.ssh.exec_command(command)
                self.showSSHOutPutLongRunningCommand(stdout)
                self.showSSHOutPutLongRunningCommand(stderr)
            else:
                command="kubectl describe pod "+podName
                stdin,stdout, stderr = self.ssh.exec_command(command)
                self.showSSHOutPutLongRunningCommand(stdout)
                self.showSSHOutPutLongRunningCommand(stderr)
               
            
        except Exception as e:
            print(e)
            print("No such pod: "+podName)

    def createDeployMent(self):
        print(Fore.BLUE+"******************* Create a deployment from the following images: **************** ")
        print("1. nginx:1.22.1")
        print("2. busybox:1.34.1")
        imagename=input("Enter 1 for nginx:1.22.1 or 2 for busybox:1.34.1: ")
        if(imagename=="1"):
            print(Fore.GREEN+"**************** Creating deployment for nginx:1.22.1 ****************")
            stdin,stdout, stderr= self.ssh.exec_command("kubectl apply -f nginxfiles/deployment.yaml")
            print(Fore.GREEN+"************ Deployment created  for nginx for nginx:1.22.1 ***************************")
            podName="nginx-deployment"
            print(Style.RESET_ALL)
            self.showSSHOutput(stdout.readlines())
            self.showSSHOutput(stderr.readlines())
            self.describePod(podName)
           
        elif(imagename=="2"):
            imagename="busybox:1.34.1"
            print(Fore.GREEN+"**************** Creating deployment for busybox:1.34.1 ****************")
            stdin,stdout, stderr= self.ssh.exec_command("kubectl apply -f busybox/deployment.yaml")
            podName="busybox-deployment"
            print(Style.RESET_ALL)
            self.showSSHOutput(stdout.readlines())
            self.showSSHOutput(stderr.readlines())
            self.describePod(podName)
           
        else:
             print(Fore.RED+"Invalid image name, please enter a valid image name")
             print(Style.RESET_ALL)

    def listDeployments(self):
        print(Fore.BLUE+"******************* The current active deployments are *******************")
        print(Style.RESET_ALL)
        stdin,stdout, stderr = self.ssh.exec_command(' kubectl get deploy ')
        self.showSSHOutPutLongRunningCommand(stdout)
        self.showSSHOutput(stdout.readlines())


    def scaleDeployment(self):
        self.listDeployments()
        deploymentName=input(Fore.BLUE+"Enter the name of the deployment you want to scale: ")
        scalingFactor=int(input("Enter the scaling factor in range 1 to 5 : "))
        if(scalingFactor < 1 or scalingFactor > 5):
            print(Fore.RED+"*******************  Invalid scaling | factor beyond allowed range  **********************   ")
            print(Style.RESET_ALL)
            return

        else:
            command ="kubectl scale deployment "+deploymentName+" --replicas="+str(scalingFactor)
            print(Fore.GREEN+"*******************  Scaling the deployment {deployment} to {scale} pods  **********************   ".format(deployment=deploymentName,scale=scalingFactor))
            print(Style.RESET_ALL)
            try:
                stdin,stdout, stderr= self.ssh.exec_command(command)
                self.showSSHOutput(stdout.readlines())
                self.showSSHOutput(stderr.readlines())
                self.describePod(deploymentName)
            except Exception as e:
                print(e)

    def perFormRollingUpdate(self):
        self.listDeployments()
        deploymentName=input(Fore.BLUE+"Enter the name of the deployment you want to perform rolling update on: ")
        print(Fore.GREEN+"*******************  Performing rolling update on deployment {deployment}  **********************   ".format(deployment=deploymentName))
        try:
            if(deploymentName!="nginx-deployment" or deploymentName!="busybox-deployment"):
                print(Fore.RED+"*******************  Invalid deployment name  **********************   ")
                return
            else:
                if(deploymentName=="nginx-deployment"):
                    print(Fore.GREEN+"******************* Updating nginx:1.22.1  deployment to nginx:1.9.1  **********************   ")
                    print(Style.RESET_ALL)
                    stdin,stdout, stderr= self.ssh.exec_command("kubectl set image deployment nginx-deployment  nginx=nginx:1.9.1")
                    self.showSSHOutput(stdout.readlines())
                    self.showSSHOutput(stderr.readlines())
                    
                    print(Fore.GREEN+"*******************  Rolling update completed  **********************   ")
                    print(Style.RESET_ALL)
                    stdin,stdout, stderr= self.ssh.exec_command(" kubectl rollout status deployment nginx-deployment")
                    self.showSSHOutput(stdout.readlines())
                    self.showSSHOutput(stderr.readlines())
                else:
                    deploymentName="busybox-deployment"
                    print(Fore.GREEN+"******************* Updating busybox:1.34.1 deployment to busybox:1.35.0  ********************** ")
                    print(Style.RESET_ALL)
                    stdin,stdout, stderr= self.ssh.exec_command("kubectl set image deployment busybox-deployment  busybox=busybox:1.35.0")
                    self.showSSHOutput(stdout.readlines())
                    self.showSSHOutput(stderr.readlines())
                    
                    print(Fore.GREEN+"*******************  Rolling update completed  **********************   ")
                    print(Style.RESET_ALL)
                    stdin,stdout, stderr= self.ssh.exec_command("kubectl rollout status deployment busybox-deployment")
                    self.showSSHOutput(stdout.readlines())
                    self.showSSHOutput(stderr.readlines())
        except Exception as e:
            print(Fore.RED+"*******************  Error: "+e+"  **********************   ")
            print(Style.RESET_ALL)

    def createPodOnEachNode(self):
        print(Fore.GREEN+"*******************  Creating a pod on each node  **********************   ")
        print(Fore.BLUE+"1. Single Container Pod")
        print("2. Multi container Pod")
        print("3. Init container Pod")
        print("4.Sidecar container Pod")
        print(Style.RESET_ALL)
        containerType = input("Enter the number corresponding to the type of container you want to create: ")
        if(containerType=="1"):
            print(Fore.GREEN+"*******************  Creating a single container pod  **********************   ")
            stdin,stdout, stderr= self.ssh.exec_command("kubectl apply -f daemonset/singlecontainer.yaml")
            self.showSSHOutput(stdout.readlines())
            self.showSSHOutput(stderr.readlines())
            print(Fore.GREEN+"*******************Single container pod Created **********************")
            print(Style.RESET_ALL)
            stdin,stdout, stderr= self.ssh.exec_command(" kubectl get deployment -n singlecontainer")
            self.showSSHOutPutLongRunningCommand(stdout)
            self.showSSHOutPutLongRunningCommand(stderr)
            stdin,stdout, stderr= self.ssh.exec_command("kubectl describe  deployment -n singlecontainer")
            self.showSSHOutPutLongRunningCommand(stdout)
            self.showSSHOutPutLongRunningCommand(stderr)
        elif(containerType=="2"):
            print(Fore.GREEN+"*******************  Creating a multi container pod  **********************   ")
            stdin,stdout, stderr= self.ssh.exec_command("kubectl apply -f daemonset/multicontainer.yaml")
            self.showSSHOutput(stdout.readlines())
            self.showSSHOutput(stderr.readlines())
            print(Fore.GREEN+"*******************Multi container pod Created **********************")
            print(Style.RESET_ALL)
            stdin,stdout, stderr= self.ssh.exec_command(" kubectl get deployment -n multicontainer")
            self.showSSHOutPutLongRunningCommand(stdout)
            self.showSSHOutPutLongRunningCommand(stderr)
            stdin,stdout, stderr= self.ssh.exec_command("kubectl describe  deployment -n multicontainer")
            self.showSSHOutPutLongRunningCommand(stdout)
            self.showSSHOutPutLongRunningCommand(stderr)
        elif(containerType=="3"):
            print(Fore.GREEN+"*******************  Creating a init container pod  **********************   ")
            stdin,stdout, stderr= self.ssh.exec_command("kubectl apply -f daemonset/initcontainer.yaml")
            self.showSSHOutput(stdout.readlines())
            self.showSSHOutput(stderr.readlines())
            print(Fore.GREEN+"*******************Init container pod Created **********************")
            print(Style.RESET_ALL)
            stdin,stdout, stderr= self.ssh.exec_command(" kubectl get pods")
            self.showSSHOutPutLongRunningCommand(stdout)
            self.showSSHOutPutLongRunningCommand(stderr)
            stdin,stdout, stderr= self.ssh.exec_command("kubectl describe pods initcontainer")
            self.showSSHOutPutLongRunningCommand(stdout)
            self.showSSHOutPutLongRunningCommand(stderr)
        
        elif containerType=="4":
            print(Fore.GREEN+"*******************  Creating a sidecar container pod  **********************   ")
            stdin,stdout, stderr= self.ssh.exec_command("kubectl apply -f daemonset/sidecarcontainer.yaml")
            self.showSSHOutput(stdout.readlines())
            self.showSSHOutput(stderr.readlines())
            print(Fore.GREEN+"*******************Sidecar container pod Created **********************")
            print(Style.RESET_ALL)
            stdin,stdout, stderr= self.ssh.exec_command(" kubectl get pods")
            self.showSSHOutPutLongRunningCommand(stdout)
            self.showSSHOutPutLongRunningCommand(stderr)
            stdin,stdout, stderr= self.ssh.exec_command("kubectl describe pods sidecarcontainer")
            self.showSSHOutPutLongRunningCommand(stdout)
            self.showSSHOutPutLongRunningCommand(stderr)
        
        else:
            print(Fore.RED+"*******************  Invalid option  **********************   ")
            print(Style.RESET_ALL)

    def runPredefinedScenario(self):
        print(Fore.GREEN+"*******************  Running predefined scenario  **********************   ")
        print(Fore.BLUE+"******************* Creating NodePort service for the Deployment **********************")
        print(Style.RESET_ALL)
        stdin,stdout, stderr= self.ssh.exec_command("kubectl apply -f daemonset/clusterservice.yaml")
        self.showSSHOutput(stdout.readlines())
        print("******************* NodePort service created **********************")
        print("******************* Now creating pods of two different types ******************")
        stdin,stdout, stderr= self.ssh.exec_command("kubectl apply -f daemonset/cluster.yaml")
        self.showSSHOutput(stdout.readlines())
        self.showSSHOutput(stderr.readlines())

        print(Fore.BLUE+"******************* Pods created **********************")
        print(Style.RESET_ALL)
        stdin,stdout, stderr= self.ssh.exec_command("kubectl get pods")
        self.showSSHOutPutLongRunningCommand(stdout)
        self.showSSHOutPutLongRunningCommand(stderr)


        print(Fore.BLUE+"******************* Verifying services are created and are communicating via cluster Ips **********************")
        print(Style.RESET_ALL)
        stdin,stdout, stderr= self.ssh.exec_command("kubectl get services")
        self.showSSHOutPutLongRunningCommand(stdout)
        self.showSSHOutPutLongRunningCommand(stderr)

        print(Fore.BLUE+"******************* Detailed Description **********************")
        print(Style.RESET_ALL)
        stdin,stdout, stderr= self.ssh.exec_command("kubectl get service web-service -o yaml")
        self.showSSHOutPutLongRunningCommand(stdout)

        stdin,stdout, stderr= self.ssh.exec_command("kubectl get service web-nodeport-service  -o yaml")
        self.showSSHOutPutLongRunningCommand(stdout)

        
            



#kubectl delete deployment dummy  -n dummy  //delete deployments









    

    
        