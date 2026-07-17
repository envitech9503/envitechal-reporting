# Auto-generated 18-07-2026: split of monolithic views.py (EnviTechAL rehab).
# Do not add module-level state here without reading views/__init__.py linker notes.
import ast
import io
import re
from django.shortcuts import render, redirect
from EnviTechAlApp.models import *
from django.core import serializers
import json
from QC.models import *
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
from datetime import datetime
from fpdf import FPDF
import base64
from io import BytesIO
from django.shortcuts import render, get_object_or_404
import os

logger = logging.getLogger(__name__)





active_users = User.objects.filter(is_active=True)
signs = Signatures.objects.filter(user__in=active_users)





























































# PARAMETER_MAPPING = {
#     # Sequence matches your table exactly (water_sr1 to water_sr32)
#     "checkinp95": {"name": "pH", "field": "water_sr1"},  # 01. pH @ 25°C
#     "checkinp65": {"name": "TDS", "field": "water_sr2"},  # 02. Total Dissolved Solids (TDS)
#     "checkinp64": {"name": "Total Hardness", "field": "water_sr3"},  # 03. Total Hardness as CaCO3
#     "checkinp60": {"name": "Color", "field": "water_sr4"},  # 04. Color
#     "checkinp63": {"name": "Turbidity", "field": "water_sr5"},  # 05. Turbidity
#     "checkinp79": {"name": "Nitrite", "field": "water_sr6"},  # 06. Nitrite
#     "checkinp77": {"name": "Nitrite", "field": "water_sr7"},  # 07. Nitrate (NO3)
#     "checkinp61": {"name": "Taste", "field": "water_sr8"},  # 08. Taste
#     "checkinp62": {"name": "Odor", "field": "water_sr9"},  # 09. Odor
#     "checkinp68": {"name": "Chloride", "field": "water_sr10"},  # 10. Chloride (Cl)
#     "checkinp66": {"name": "Fluoride", "field": "water_sr11"},  # 11. Fluoride (F)
#     "checkinp72": {"name": "Aluminium", "field": "water_sr12"},  # 12. Aluminum (Al)
#     "checkinp76": {"name": "Nickel", "field": "water_sr13"},  # 13. Nickel (Ni)
#     "checkinp75": {"name": "Lead", "field": "water_sr14"},  # 14. Lead (Pb)
#     # Note: 15. Barium (Ba) - no corresponding checkbox in your form
#     "checkinp71": {"name": "Antimony", "field": "water_sr16"},  # 16. Antimony (Sb)
#     "checkinp73": {"name": "Arsenic", "field": "water_sr17"},  # 17. Arsenic (As)
#     "checkinp74": {"name": "Boron", "field": "water_sr18"},  # 18. Boron (B)
#     # Note: 19. Cadmium (Cd) - no corresponding checkbox in your form
#     "checkinp67": {"name": "Chromium", "field": "water_sr20"},  # 20. Chromium (Cr)
#     "checkinp80": {"name": "Selenium", "field": "water_sr21"},  # 21. Selenium (Se)
#     "checkinp70": {"name": "Copper", "field": "water_sr22"},  # 22. Copper (Cu)
#     "checkinp69": {"name": "Cyanide", "field": "water_sr23"},  # 23. Cyanide (CN)
#     "checkinp78": {"name": "Mercury", "field": "water_sr24"},  # 24. Mercury (Hg)
#     # Note: 25. Manganese (Mn) - no corresponding checkbox in your form
#     "checkinp82": {"name": "Zinc", "field": "water_sr26"},  # 26. Zinc (Zn)
#     "checkinp81": {"name": "Residual Chlorine", "field": "water_sr27"},  # 27. Residual Chlorine
#     "checkinp86": {"name": "Phenol", "field": "water_sr28"},  # 28. Phenolic Compounds as Phenols
#     "checkinp100": {"name": "Faecal coliform", "field": "water_sr29"},  # 29. Fecal Coliform
#     "checkinp98": {"name": "Coliform", "field": "water_sr30"},  # 30. Total Coliform
#     "checkinp99": {"name": "E.coli", "field": "water_sr31"},  # 31. E-Coli
#     # Note: 32. Pesticides - no corresponding checkbox in your form
# }

# PARAMETER_MAPPING = {
#     # Original mappings
#     "checkinp95": {"name": "pH", "field": "water_sr1"},
#     "checkinp65": {"name": "TDS", "field": "water_sr2"},
#     "checkinp64": {"name": "Total Hardness", "field": "water_sr3"},
#     "checkinp60": {"name": "Color", "field": "water_sr4"},
#     "checkinp63": {"name": "Turbidity", "field": "water_sr5"},
#     "checkinp79": {"name": "Nitrite", "field": "water_sr6"},
#     "checkinp77": {"name": "Nitrate", "field": "water_sr7"},
#     "checkinp61": {"name": "Taste", "field": "water_sr8"},
#     "checkinp62": {"name": "Odor", "field": "water_sr9"},
#     "checkinp68": {"name": "Chloride", "field": "water_sr10"},
#     "checkinp66": {"name": "Fluoride", "field": "water_sr11"},
#     "checkinp72": {"name": "Aluminium", "field": "water_sr12"},
#     "checkinp76": {"name": "Nickel", "field": "water_sr13"},
#     "checkinp75": {"name": "Lead", "field": "water_sr14"},
#     "checkinp71": {"name": "Antimony", "field": "water_sr16"},
#     "checkinp73": {"name": "Arsenic", "field": "water_sr17"},
#     "checkinp74": {"name": "Boron", "field": "water_sr18"},
#     "checkinp67": {"name": "Chromium", "field": "water_sr20"},
#     "checkinp80": {"name": "Selenium", "field": "water_sr21"},
#     "checkinp70": {"name": "Copper", "field": "water_sr22"},
#     "checkinp69": {"name": "Cyanide", "field": "water_sr23"},
#     "checkinp78": {"name": "Mercury", "field": "water_sr24"},
#     "checkinp82": {"name": "Zinc", "field": "water_sr26"},
#     "checkinp81": {"name": "Residual Chlorine", "field": "water_sr27"},
#     "checkinp86": {"name": "Phenol", "field": "water_sr28"},
#     "checkinp100": {"name": "Faecal coliform", "field": "water_sr29"},
#     "checkinp98": {"name": "Coliform", "field": "water_sr30"},
#     "checkinp99": {"name": "E.coli", "field": "water_sr31"},
    
#     # Missing original parameters that need to be mapped
#     "checkinp87": {"name": "Sodium", "field": "water_sr93"},
#     "checkinp94": {"name": "Magnesium", "field": "water_sr94"},
#     "checkinp101": {"name": "Pseudomonas aeruginosa", "field": "water_sr95"},
#     "checkinp88": {"name": "Acidity", "field": "water_sr96"},
#     "checkinp83": {"name": "DO", "field": "water_sr97"},
#     "checkinp89": {"name": "Potassium", "field": "water_sr98"},
#     "checkinp90": {"name": "Carbonates", "field": "water_sr99"},
#     "checkinp96": {"name": "Sulphate", "field": "water_sr100"},
#     "checkinp84": {"name": "Conductivity", "field": "water_sr101"},
#     "checkinp91": {"name": "Bicarbonates", "field": "water_sr102"},
#     "checkinp97": {"name": "Silica", "field": "water_sr103"},
#     "checkinp102": {"name": "Total Bacterial count", "field": "water_sr104"},
#     "checkinp85": {"name": "TKN", "field": "water_sr105"},
#     "checkinp92": {"name": "Alkalinity", "field": "water_sr106"},
#     "checkinp93": {"name": "Calcium", "field": "water_sr107"},
#     "checkinp103": {"name": "others", "field": "water_sr108"},
    
#     # Other parameter mappings (other_param_1 to other_param_64)
#     "other1": {"name": "Barium", "field": "water_sr15"},
#     "other2": {"name": "Manganese", "field": "water_sr25"},
#     "other3": {"name": "Cadmium", "field": "water_sr19"},
#     "other4": {"name": "Silver", "field": "water_sr32"},
#     "other5": {"name": "Reactive Silica", "field": "water_sr33"},
#     "other6": {"name": "Silicic Acid", "field": "water_sr34"},
#     "other7": {"name": "COD", "field": "water_sr35"},
#     "other8": {"name": "BOD", "field": "water_sr36"},
#     "other9": {"name": "Cobalt", "field": "water_sr37"},
#     "other10": {"name": "Polyaromatic Hydrocarbons (PAH)", "field": "water_sr38"},
#     "other11": {"name": "Pesticides", "field": "water_sr39"},
#     "other12": {"name": "Oil & Grease", "field": "water_sr40"},
#     "other13": {"name": "Alpha Emitters", "field": "water_sr41"},
#     "other14": {"name": "Beta Emitters", "field": "water_sr42"},
#     "other15": {"name": "Salinity", "field": "water_sr43"},
#     "other16": {"name": "Resistivity", "field": "water_sr44"},
#     "other17": {"name": "TOC", "field": "water_sr45"},
#     "other18": {"name": "VOC", "field": "water_sr46"},
#     "other19": {"name": "Phosphorus", "field": "water_sr47"},
#     "other20": {"name": "Calcium Hardness", "field": "water_sr48"},
#     "other21": {"name": "Magnesium Hardness", "field": "water_sr49"},
#     "other22": {"name": "Carbonate Hardness", "field": "water_sr50"},
#     "other23": {"name": "Non-Carbonate Hardness", "field": "water_sr51"},
#     "other24": {"name": "Temporary Hardness", "field": "water_sr52"},
#     "other25": {"name": "Strontium", "field": "water_sr53"},
#     "other26": {"name": "Chromium III", "field": "water_sr54"},
#     "other27": {"name": "Chromium VI", "field": "water_sr55"},
#     "other28": {"name": "Iron", "field": "water_sr56"},
#     "other29": {"name": "Ferrous (Fe+2)", "field": "water_sr57"},
#     "other30": {"name": "Ferric (Fe+3)", "field": "water_sr58"},
#     "other31": {"name": "Ammonia", "field": "water_sr59"},
#     "other32": {"name": "Tin", "field": "water_sr60"},
#     "other33": {"name": "Ammonium", "field": "water_sr61"},
#     "other34": {"name": "Free CO2", "field": "water_sr62"},
#     "other35": {"name": "Hydroxide Alkalinity as CaCO3", "field": "water_sr63"},
#     "other36": {"name": "Methyl Orange Alkalinity as CaCO3", "field": "water_sr64"},
#     "other37": {"name": "Phenolphthalein Alkalinity as CaCO3", "field": "water_sr65"},
#     "other38": {"name": "Particulate Matter", "field": "water_sr66"},
#     "other39": {"name": "Silt Density Index", "field": "water_sr67"},
#     "other40": {"name": "Particles Size", "field": "water_sr68"},
#     "other41": {"name": "AOx", "field": "water_sr69"},
#     "other42": {"name": "Chlorine", "field": "water_sr70"},
#     "other43": {"name": "Free Chlorine", "field": "water_sr71"},
#     "other44": {"name": "Sulphide", "field": "water_sr72"},
#     "other45": {"name": "Total Solid", "field": "water_sr73"},
#     "other46": {"name": "Beryllium", "field": "water_sr74"},
#     "other49": {"name": "Phosphate", "field": "water_sr75"},
#     "other50": {"name": "Volatile Suspended Solids (VSS)", "field": "water_sr76"},
#     "other51": {"name": "Settleable solids (Imhoff cone)", "field": "water_sr77"},
#     "other52": {"name": "Oxidation–Reduction Potential (ORP)", "field": "water_sr78"},
#     "other53": {"name": "Volatile Organic Halogens (VOX)", "field": "water_sr79"},
#     "other54": {"name": "Sodium Adsorption Ratio (SAR)", "field": "water_sr80"},
#     "other55": {"name": "Residual Sodium Carbonate (RSC)", "field": "water_sr81"},
#     "other56": {"name": "Temperature", "field": "water_sr82"},
#     "other57": {"name": "TSS", "field": "water_sr83"},
#     "other58": {"name": "Anionic Surfactants as MBAS", "field": "water_sr84"},
#     "other59": {"name": "Total Plate Count", "field": "water_sr85"},
#     "other60": {"name": "Legionella", "field": "water_sr86"},
#     "other61": {"name": "Fecal Enterococci", "field": "water_sr87"},
#     "other62": {"name": "Heterotrophic Bacteria", "field": "water_sr88"},
#     "other63": {"name": "Enterobacteriaceae", "field": "water_sr89"},
#     "other64": {"name": "Listeria Spp.", "field": "water_sr90"},
#     "other65": {"name": "Salmonella", "field": "water_sr91"},
#     "other66": {"name": "Yeasts & Molds", "field": "water_sr92"},
# }


# PARAMETER_MAPPING = {
#     "checkinp60": {"name": "Color", "field": "water_sr4"},
#     "checkinp61": {"name": "Taste", "field": "water_sr8"},
#     "checkinp62": {"name": "Odor", "field": "water_sr9"},
#     "checkinp63": {"name": "Turbidity", "field": "water_sr5"},
#     "checkinp64": {"name": "Total Hardness*", "field": "water_sr3"},
#     "checkinp65": {"name": "TDS", "field": "water_sr2"},
#     "checkinp66": {"name": "Fluoride*", "field": "water_sr11"},
#     "checkinp67": {"name": "Chromium", "field": "water_sr8"},
#     "checkinp68": {"name": "Chloride", "field": "water_sr10"},
#     "checkinp69": {"name": "Cyanide", "field": "water_sr23"},
#     "checkinp70": {"name": "Copper", "field": "water_sr22"},
#     "checkinp71": {"name": "Antimony", "field": "water_sr16"},
#     "checkinp72": {"name": "Aluminium", "field": "water_sr12"},
#     "checkinp73": {"name": "Arsenic", "field": "water_sr17"},
#     "checkinp74": {"name": "Boron", "field": "water_sr18"},
#     "checkinp75": {"name": "Lead", "field": "water_sr14"},
#     "checkinp76": {"name": "Nickel*", "field": "water_sr13"},
#     "checkinp77": {"name": "Nitrate*", "field": "water_sr7"},
#     "checkinp78": {"name": "Mercury", "field": "water_sr24"},
#     "checkinp79": {"name": "Nitrite", "field": "water_sr6"},
#     "checkinp80": {"name": "Selenium", "field": "water_sr21"},
#     "checkinp81": {"name": "Residual Chlorine", "field": "water_sr27"},
#     "checkinp82": {"name": "Zinc", "field": "water_sr26"},
#     "checkinp83": {"name": "DO", "field": "water_sr24"},
#     "checkinp84": {"name": "Conductivity", "field": "water_sr25"},
#     "checkinp85": {"name": "TKN", "field": ""},
#     "checkinp86": {"name": "Phenol", "field": "water_sr28"},
#     "checkinp87": {"name": "Sodium*", "field": ""},
#     "checkinp88": {"name": "Acidity", "field": "water_sr29"},
#     "checkinp89": {"name": "Potassium", "field": ""},
#     "checkinp90": {"name": "Carbonates", "field": ""},
#     "checkinp91": {"name": "Bicarbonates", "field": ""},
#     "checkinp92": {"name": "Alkalinity*", "field": "water_sr33"},
#     "checkinp93": {"name": "Calcium*", "field": "water_sr34"},
#     "checkinp94": {"name": "Magnesium*", "field": "water_sr35"},
#     "checkinp95": {"name": "pH*", "field": "water_sr36"},
#     "checkinp96": {"name": "Sulphate*", "field": "water_sr37"},
#     "checkinp97": {"name": "Silica", "field": "water_sr38"},
#     "checkinp98": {"name": "Coliform", "field": "water_sr30"},
#     "checkinp99": {"name": "E.coli", "field": "water_sr31"},
#     "checkinp100": {"name": "Faecal coliform", "field": "water_sr29"},
#     "checkinp101": {"name": "Pseudomonas aeruginosa", "field": ""},
#     "checkinp102": {"name": "Total Bacterial count", "field": ""},
#     "checkinp103": {"name": "Others", "field": "other2"},

#     # Extra / Other parameters
#     "other_param_1": {"name": "Barium", "field": "water_sr15"},
#     "other_param_2": {"name": "Manganese", "field": "water_sr25"},
#     "other_param_3": {"name": "Cadmium", "field": "water_sr19"},
#     "other_param_4": {"name": "Silver", "field": ""},
#     "other_param_5": {"name": "Reactive Silica", "field": ""},
#     "other_param_6": {"name": "Silicic Acid", "field": ""},
#     "other_param_7": {"name": "COD", "field": "water_sr50"},
#     "other_param_8": {"name": "BOD", "field": "water_sr51"},
#     "other_param_9": {"name": "Cobalt", "field": "water_sr52"},
#     "other_param_10": {"name": "Polyaromatic Hydrocarbons (PAH)", "field": "water_sr53"},
#     "other_param_11": {"name": "Pesticides", "field": "water_sr32"},
#     "other_param_12": {"name": "Oil & Grease", "field": "water_sr55"},
#     "other_param_13": {"name": "Alpha Emitters", "field": "water_sr56"},
#     "other_param_14": {"name": "Beta Emitters", "field": "water_sr57"},
#     "other_param_15": {"name": "Salinity", "field": "water_sr58"},
#     "other_param_16": {"name": "Resistivity", "field": "water_sr59"},
#     "other_param_17": {"name": "TOC", "field": "water_sr60"},
#     "other_param_18": {"name": "VOC", "field": "water_sr61"},
#     "other_param_19": {"name": "Phosphorus", "field": "water_sr62"},
#     "other_param_20": {"name": "Calcium Hardness", "field": "water_sr63"},
#     "other_param_21": {"name": "Magnesium Hardness", "field": "water_sr64"},
#     "other_param_22": {"name": "Carbonate Hardness", "field": "water_sr65"},
#     "other_param_23": {"name": "Non-Carbonate Hardness", "field": "water_sr66"},
#     "other_param_24": {"name": "Temporary Hardness", "field": "water_sr67"},
#     "other_param_25": {"name": "Strontium", "field": "water_sr68"},
#     "other_param_26": {"name": "Chromium III", "field": "water_sr20"},
#     "other_param_27": {"name": "Chromium VI", "field": "water_sr21"},
#     "other_param_28": {"name": "Iron", "field": "water_sr71"},
#     "other_param_29": {"name": "Ferrous (Fe+2)", "field": "water_sr72"},
#     "other_param_30": {"name": "Ferric (Fe+3)", "field": "water_sr73"},
#     "other_param_31": {"name": "Ammonia", "field": "water_sr74"},
#     "other_param_32": {"name": "Tin", "field": "water_sr75"},
#     "other_param_33": {"name": "Ammonium", "field": "water_sr76"},
#     "other_param_34": {"name": "Free CO2", "field": "water_sr77"},
#     "other_param_35": {"name": "Hydroxide Alkalinity as CaCO3", "field": "water_sr78"},
#     "other_param_36": {"name": "Methyl Orange Alkalinity as CaCO3", "field": "water_sr79"},
#     "other_param_37": {"name": "Phenolphthalein Alkalinity as CaCO3", "field": "water_sr80"},
#     "other_param_38": {"name": "Particulate Matter", "field": "water_sr81"},
#     "other_param_39": {"name": "Silt Density Index", "field": "water_sr82"},
#     "other_param_40": {"name": "Particles Size", "field": "water_sr83"},
#     "other_param_41": {"name": "AOx", "field": "water_sr84"},
#     "other_param_42": {"name": "Chlorine", "field": "water_sr85"},
#     "other_param_43": {"name": "Free Chlorine", "field": "water_sr86"},
#     "other_param_44": {"name": "Sulphide", "field": "water_sr87"},
#     "other_param_45": {"name": "Total Solid", "field": "water_sr88"},
#     "other_param_46": {"name": "Beryllium", "field": "water_sr89"},
#     "other_param_47": {"name": "Phosphate", "field": "water_sr90"},
#     "other_param_48": {"name": "Volatile Suspended Solids (VSS)", "field": "water_sr91"},
#     "other_param_49": {"name": "Settleable solids (Imhoff cone)", "field": "water_sr92"},
#     "other_param_50": {"name": "Oxidation–Reduction Potential (ORP)", "field": "water_sr93"},
#     "other_param_51": {"name": "Volatile Organic Halogens (VOX)", "field": "water_sr94"},
#     "other_param_52": {"name": "Sodium Adsorption Ratio (SAR)", "field": "water_sr95"},
#     "other_param_53": {"name": "Residual Sodium Carbonate (RSC)", "field": "water_sr96"},
#     "other_param_54": {"name": "Temperature", "field": "water_sr97"},
#     "other_param_55": {"name": "TSS", "field": "water_sr98"},
#     "other_param_56": {"name": "Anionic Surfactants as MBAS", "field": "water_sr99"},
#     "other_param_57": {"name": "Total Plate Count", "field": "water_sr100"},
#     "other_param_58": {"name": "Legionella", "field": "water_sr101"},
#     "other_param_59": {"name": "Fecal Enterococci", "field": "water_sr102"},
#     "other_param_60": {"name": "Heterotrophic Bacteria", "field": "water_sr103"},
#     "other_param_61": {"name": "Enterobacteriaceae", "field": "water_sr104"},
#     "other_param_62": {"name": "Listeria Spp.", "field": "water_sr105"},
#     "other_param_63": {"name": "Salmonella", "field": "water_sr106"},
#     "other_param_64": {"name": "Yeasts & Molds", "field": "water_sr107"},
# }


PARAMETER_MAPPING = {
    "checkinp60": {"name": "Color", "field": "water_sr4"},
    "checkinp61": {"name": "Taste", "field": "water_sr8"},
    "checkinp62": {"name": "Odor", "field": "water_sr9"},
    "checkinp63": {"name": "Turbidity", "field": "water_sr5"},
    "checkinp64": {"name": "Total Hardness*", "field": "water_sr3"},
    "checkinp65": {"name": "TDS", "field": "water_sr2"},
    "checkinp66": {"name": "Fluoride*", "field": "water_sr11"},
    "checkinp67": {"name": "Chromium", "field": "water_sr20"},  # Fixed: was water_sr8 (duplicate with Taste)
    "checkinp68": {"name": "Chloride", "field": "water_sr10"},
    "checkinp69": {"name": "Cyanide", "field": "water_sr23"},
    "checkinp70": {"name": "Copper", "field": "water_sr22"},
    "checkinp71": {"name": "Antimony", "field": "water_sr16"},
    "checkinp72": {"name": "Aluminium", "field": "water_sr12"},
    "checkinp73": {"name": "Arsenic", "field": "water_sr17"},
    "checkinp74": {"name": "Boron", "field": "water_sr18"},
    "checkinp75": {"name": "Lead", "field": "water_sr14"},
    "checkinp76": {"name": "Nickel*", "field": "water_sr13"},
    "checkinp77": {"name": "Nitrate*", "field": "water_sr7"},
    "checkinp78": {"name": "Mercury", "field": "water_sr24"},
    "checkinp79": {"name": "Nitrite", "field": "water_sr6"},
    "checkinp80": {"name": "Selenium", "field": "water_sr21"},
    "checkinp81": {"name": "Residual Chlorine", "field": "water_sr27"},
    "checkinp82": {"name": "Zinc", "field": "water_sr26"},
    # "checkinp83": {"name": "DO", "field": ""},  # No direct field
    # "checkinp84": {"name": "Conductivity", "field": ""},  # No direct field
    # "checkinp85": {"name": "TKN", "field": ""},  # No direct field
    "checkinp86": {"name": "Phenol", "field": "water_sr28"},
    # "checkinp87": {"name": "Sodium*", "field": ""},  # No direct field
    # "checkinp88": {"name": "Acidity", "field": ""},  # No direct field
    # "checkinp89": {"name": "Potassium", "field": ""},  # No direct field
    # "checkinp90": {"name": "Carbonates", "field": ""},  # No direct field
    # "checkinp91": {"name": "Bicarbonates", "field": ""},  # No direct field
    # "checkinp92": {"name": "Alkalinity*", "field": ""},  # No direct field (was water_sr33)
    # "checkinp93": {"name": "Calcium*", "field": ""},  # No direct field (was water_sr34)
    # "checkinp94": {"name": "Magnesium*", "field": ""},  # No direct field (was water_sr35)
    "checkinp95": {"name": "pH*", "field": "water_sr1"},  # Fixed: was water_sr36
    # "checkinp96": {"name": "Sulphate*", "field": ""},  # No direct field (was water_sr37)
    # "checkinp97": {"name": "Silica", "field": ""},  # No direct field (was water_sr38)
    "checkinp98": {"name": "Coliform", "field": "water_sr30"},
    "checkinp99": {"name": "E.coli", "field": "water_sr31"},
    "checkinp100": {"name": "Faecal coliform", "field": "water_sr29"},
    # "checkinp101": {"name": "Pseudomonas aeruginosa", "field": ""},  # No direct field
    # "checkinp102": {"name": "Total Bacterial count", "field": ""},  # No direct field
   

    # Extra / Other parameters - Only those with actual database fields
    "other_param_1": {"name": "Barium", "field": "water_sr15"},
    "other_param_2": {"name": "Manganese", "field": "water_sr25"},
    "other_param_3": {"name": "Cadmium", "field": "water_sr19"},
    "other_param_11": {"name": "Pesticides", "field": "water_sr32"},
    "other_param_26": {"name": "Chromium", "field": "water_sr20"},  # Same as Chromium
    "other_param_27": {"name": "Selenium", "field": "water_sr21"},  # Same as Selenium - CONFLICT!
    
    
}

# Export everything (incl. underscore helpers) to family modules.
__all__ = [_k for _k in list(globals()) if not _k.startswith("__")]
