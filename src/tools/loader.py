import os
import sys
import importlib
import logging
import json

logger = logging.getLogger(__name__)

# List to hold the actual Python callable functions.
# Gemini SDK can automatically inspect Python functions (docstrings, type hints)
# to generate the Tool declarations.
plugin_registry = {
    "tools": []
}

def load_plugins():
    tools_dir = os.path.dirname(__file__)
    if not os.path.exists(tools_dir):
        return plugin_registry
    
    # Iterate through directories in tools/
    for item in os.listdir(tools_dir):
        plugin_path = os.path.join(tools_dir, item)
        if os.path.isdir(plugin_path) and item != "__pycache__":
            plugin_file = os.path.join(plugin_path, "plugin.py")
            if os.path.exists(plugin_file):
                try:
                    # Dynamically import the module
                    module_name = f"tools.{item}.plugin"
                    if module_name not in sys.modules:
                         # Ensure the tools directory is in path for import
                         sys.path.insert(0, os.path.dirname(tools_dir))
                    
                    # Check environment requirements
                    config_file = os.path.join(plugin_path, "config.json")
                    if os.path.exists(config_file):
                        with open(config_file, 'r', encoding='utf-8') as f:
                            plugin_config = json.load(f)
                        
                        env_reqs = plugin_config.get("env_requirements", [])
                        missing_envs = [env for env in env_reqs if env not in os.environ]
                        if missing_envs:
                            logger.error(f"Plugin '{item}' is missing required environment variables: {missing_envs}. Skipping load.")
                            continue

                    module = importlib.import_module(module_name)
                    
                    # Ensure the module has the required get_tools function
                    if hasattr(module, "get_tools"):
                        funcs = module.get_tools()
                        if isinstance(funcs, list):
                            plugin_registry["tools"].extend(funcs)
                            logger.info(f"Successfully loaded tools from plugin: {item}")
                        else:
                            logger.warning(f"Plugin {item} get_tools() did not return a list.")
                    else:
                        logger.warning(f"Plugin {item} is missing get_tools() function.")
                except Exception as e:
                    logger.error(f"Failed to load plugin {item}: {e}")

    return plugin_registry
