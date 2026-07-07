# %%
import logging


logging.basicConfig(level=logging.INFO)
from cellmap_flow.blockwise import CellMapFlowBlockwiseProcessor

p = "/groups/cellmap/cellmap/zouinkhim/exp_salivary/persistence/er/jrc_mus-salivary-1/20251215_er.yaml"
# %%
processor = CellMapFlowBlockwiseProcessor(p)
# %%
processor.dtype
# %%
processor.model_config.output_dtype
# %%
from cellmap_flow.globals import g

g.get_output_dtype(processor.model_config.output_dtype)
# %%
