from .kernel import DolphinDBKernel

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=DolphinDBKernel)