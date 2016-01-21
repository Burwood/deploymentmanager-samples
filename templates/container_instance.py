# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Creates a Container VM with the provided Container manifest."""
import common
import container_helper
import default
import vm_instance

# Check vm_instance for additional properties used
# Specific properties for this component, also see container_helper
C_IMAGE = default.C_IMAGE
DCKRIMAGE = default.DCKRIMAGE
SRCIMAGE = default.SRCIMAGE
METADATA = default.METADATA


def GenerateContainerInstance(context):
  """Generates an instance of container instance with the passed manifest."""
  prop = context.properties
  metadata = prop.setdefault(METADATA, dict())
  items = metadata.setdefault('items', list())
  if common.IsComputeLink(prop[C_IMAGE]):
    prop[default.SRCIMAGE] = prop[C_IMAGE]
  else:
    prop[SRCIMAGE] = common.GlobalComputeLink(
        'google-containers', 'images', prop[C_IMAGE])
  items.append(
      {
          'key': 'google-container-manifest',
          'value': '%s' % container_helper.GenerateManifest(context)
      })
  return vm_instance.GenerateComputeVM(context)


def GenerateResourceList(context):
  """Returns list of resources generated by this module."""
  resources = GenerateContainerInstance(context)
  resources += common.AddDiskResourcesIfNeeded(context)
  return resources


@common.FormatErrorsDec
def GenerateConfig(context):
  """Generates YAML resource configuration."""
  return common.MakeResource(GenerateResourceList(context))