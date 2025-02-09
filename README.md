# kalliope_trigger_openww
Openwakeword Trigger for Kalliope, see details at [dscripka/openWakeWord](https://github.com/dscripka/openWakeWord)

## Installation
```bash
kalliope install --git-url https://github.com/github10011111/kalliope_trigger_openww.git
```

## Parameters

| parameter    | required | type    | default | choices         |  comment                                   |
|--------------|----------|---------|---------|-----------------|---------------------------------------------------|
| model_file   | Yes      | string  |         |                 | Comma separated list of paths to wakeword files
| engine       | No       | string  |'tflite' | 'tflite', 'onnx'| Trigger word detection engine

## Example settings

```yaml
# This is the trigger engine that will catch your magic work to wake up Kalliope.

default_trigger: "openww"

# Trigger engine configuration
triggers:
  - openww:
      model_file: "trigger/sheila_v2.tflite,trigger/hey_honey.tflite,trigger/oww_models/alexa_v0.1.tflite"
      engine: "tflite"

```

## Available Openwakeword wake words
To install the default Openwakeword models:
In python:
```
  import openwakeword
  from openwakeword.model import Model
  openwakeword.utils.download_models()
```

There are some more available wake words [here](https://github.com/fwartner/home-assistant-wakewords-collection). 
You need the wake_word.[tflite|onnx] file and the wake_word.[tflite|onnx].json file, both need to be in the same directory. 
You will have to rename the wake_word_wake_word.[tflite|onnx].json file to wake_word.[tflite|onnx].json

## Note

You have to add the path to the trigger folder in your settings.
E.g.:
```
# ---------------------------
# resource directory path
# ---------------------------
resource_directory:
  trigger: "resources/trigger"
  neuron: "resources/neurons"
  stt: "resources/stt"
  tts: "resources/tts"
```
