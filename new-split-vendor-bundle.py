# Run me with the target config bundle path passed in - e.g. python split-config-bundle.py ".\export-profiles\PrusaSlicer_config_bundle.ini"
import sys
import os
import configparser

class Config:
    def __init__(self, fileName, contents):
        self.fileName = fileName
        self.contents = contents

def main(targetBundlePath):
    print("Looking for configuration sections in file '" + targetBundlePath + "'")

    #with open(targetBundlePath, "r") as bundleContents:
        #line = bundleContents.readline()

    testconfig = configparser.ConfigParser()
    testconfig.read(targetBundlePath)

    printConfigurationsFound = []
    filamentConfigurationsFound = []
    printerConfigurationsFound = []

    for section in testconfig.sections():
        if section.startswith("filament:"):
            print("Found filament config section: " + section)
            
            # Check if this filament config inherits from another filament config
            #if testconfig.has_option(section, 'inherits'):
                #print("Found inherits option: " + testconfig.get(section, 'inherits'))
            
            # merge filament config with inherited filament config
            if testconfig.has_option(section, 'inherits'):
                inheritedFilamentConfig = "filament:" + testconfig.get(section, 'inherits')
                print("Found inherits option: " + inheritedFilamentConfig)

                if inheritedFilamentConfig in testconfig:
                    mergedFilamentConfig = {**testconfig[inheritedFilamentConfig], **testconfig[section]}
                    print(mergedFilamentConfig)
                    filamentConfigurationsFound.append(Config(section + ".ini", mergedFilamentConfig.items()))
                
                else:
                    print("Inherited filament config '" + inheritedFilamentConfig + "' not found")


    outputDir = "export-profiles"
    for configuration in filamentConfigurationsFound:
        outputFileName = os.path.join(outputDir, configuration.fileName)

        print("Writing configuration to '" + outputFileName + "'")
        with open(outputFileName, "w") as outputFile:
            for section in configuration.contents:
                outputFile.write("[" + section[0] + "]\n")
                for option in section[1]:
                    outputFile.write(option[0] + " = " + option[1] + "\n")
                outputFile.write("\n")


        #print("Found config section: " + section)
        #printConfigurationsFound.append(Config(section + ".ini", testconfig[section]))

    #for section in testconfig.sections():
        #print("Found config section: " + section)
        #filamentConfigurationsFound.append(Config(section + ".ini", testconfig[section]))

        

    #print("Found " + str(len(filamentConfigurationsFound)) + " configurations in total")

    #print (testconfig.options(filamentConfigurationsFound))
    #print("testing section 0: " + testconfig.read_dict(configurationsFound[0]))

    
    # print (testconfig.has_section('filament:*PLA*'))
    # returns True
    



    #outputDir = "export-profiles"
    #for configuration in filamentConfigurationsFound:
        #outputFileName = os.path.join(outputDir, section + ".ini")

        #print("Writing configuration to '" + outputFileName + "'")
        #with open(outputFileName, "w") as outputFile:
            #for configLine in configuration.contents:
                #if configLine.rstrip():
                    #outputFile.write(configLine)

if __name__ == '__main__':
    main(str(sys.argv[1]))