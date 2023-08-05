"""PlotOptiX predefined materials.
"""

import os

from plotoptix.enums import RtFormat

__pkg_dir__ = os.path.dirname(__file__)

m_flat = {
      "RadianceProgram": "materials7.ptx::__closesthit__radiance__flat",
      "OcclusionProgram": "materials7.ptx::__closesthit__occlusion",
    }
"""
Super-fast material, color is not shaded anyhow. Use color components range ``<0; 1>``.
"""

m_eye_normal_cos = {
      "RadianceProgram": "materials7.ptx::__closesthit__radiance__cos",
      "OcclusionProgram": "materials7.ptx::__closesthit__occlusion",
    }
"""
Fast material, color is shaded by the cos(eye-hit-normal). Use color components range
``<0; 1>``.
"""

m_diffuse = {
      "RadianceProgram": "materials7.ptx::__closesthit__radiance__diffuse",
      "OcclusionProgram": "materials7.ptx::__closesthit__occlusion",
      "VarUInt": { "flags": 2 }
    }
"""
Lambertian diffuse material. Note it is available by default under the name "diffuse".
Use color components range ``<0; 1>``.
"""

m_matt_diffuse = {
      "RadianceProgram": "materials7.ptx::__closesthit__radiance__diffuse",
      "OcclusionProgram": "materials7.ptx::__closesthit__occlusion",
      "VarUInt": { "flags": 2 },
      "VarFloat": { "base_roughness": 1 }
    }
"""
Oren-Nayar diffuse material. Surface roughness range is ``<0; inf)``, 0 is equivalent to
the Lambertian "diffuse" material.
"""

m_transparent_diffuse = {
      "RadianceProgram": "materials7.ptx::__closesthit__radiance__diffuse_masked",
      "OcclusionProgram": "materials7.ptx::__closesthit__occlusion_transparency",
      "VarUInt": { "flags": 2 },
      "VarFloat": { "base_roughness": 0 }
    }
"""
Diffuse material with transparency set according to alpha channel of ``ColorTextures``.
Roughness can be set to Lambertian or Oren-Nayar with ``base_roughness`` parameter.
"""

m_mirror = {
      "RadianceProgram": "materials7.ptx::__closesthit__radiance__reflective",
      "OcclusionProgram": "materials7.ptx::__closesthit__occlusion",
      "VarUInt": { "flags": 6 },
      "VarFloat3": {
        "surface_albedo": [ 1.0, 1.0, 1.0 ]
      }
}
"""
Reflective mirror, quite simple to calculate and therefore fast material. Note, this material
has default values: ``reflectivity_index = 1`` and ``reflectivity_range = 1``. In this configuration
the shading algorithm overrides ``surface_albedo`` with the color assigned to each primitive (RGB
range ``<0; 1>``), which results with colorized reflections.
"""

m_metallic = {
      "RadianceProgram": "materials7.ptx::__closesthit__radiance__reflective",
      "OcclusionProgram": "materials7.ptx::__closesthit__occlusion",
      "VarUInt": { "flags": 6 },
      "VarFloat": { "base_roughness": 0.002 },
}
"""
Strongly reflective, metallic material. Note, this material has default values: ``reflectivity_index = 1``
and ``reflectivity_range = 1``. In this configuration the shading algorithm overrides ``surface_albedo``
with the color assigned to each primitive (RGB range <0; 1>), which results with colorized reflections.
Roughness of the surface should be usually small.
"""

m_transparent_metallic = {
      "RadianceProgram": "materials7.ptx::__closesthit__radiance__reflective_masked",
      "OcclusionProgram": "materials7.ptx::__closesthit__occlusion_transparency",
      "VarUInt": { "flags": 6 },
      "VarFloat": { "base_roughness": 0.002 },
}
"""
Strongly reflective, metallic material with transparency set according to alpha channel of
``ColorTextures``. See also :attr:`plotoptix.materials.m_metallic`.
"""

m_plastic = {
      "RadianceProgram": "materials7.ptx::__closesthit__radiance__reflective",
      "OcclusionProgram": "materials7.ptx::__closesthit__occlusion",
      "VarUInt": { "flags": 6 },
      "VarFloat": {
        "reflectivity_index": 0.0,
        "reflectivity_range": 0.5,
      },
      "VarFloat3": {
        "refraction_index": [ 2.0, 2.0, 2.0 ],
        "surface_albedo": [ 1.0, 1.0, 1.0 ]
      }
}
"""
Combined reflective and diffuse surface. Reflection fraction may be boosted with reflectivity_index
set above 0 (up to 1, resulting with mirror-like appearance) or minimized with a lower than default
reflectivity_range value (down to 0). Higher refraction_index gives a more glossy look.
"""

m_matt_plastic = {
      "RadianceProgram": "materials7.ptx::__closesthit__radiance__reflective",
      "OcclusionProgram": "materials7.ptx::__closesthit__occlusion",
      "VarUInt": { "flags": 6 },
      "VarFloat": {
        "reflectivity_index": 0.0,
        "reflectivity_range": 0.5,
        "base_roughness": 0.001
      },
      "VarFloat3": {
        "refraction_index": [ 2.0, 2.0, 2.0 ],
        "surface_albedo": [ 1.0, 1.0, 1.0 ]
      }
}
"""
Similar to :attr:`plotoptix.materials.m_plastic` but slightly rough surface.
"""

m_transparent_plastic = {
      "RadianceProgram": "materials7.ptx::__closesthit__radiance__reflective_masked",
      "OcclusionProgram": "materials7.ptx::__closesthit__occlusion_transparency",
      "VarUInt": { "flags": 6 },
      "VarFloat": {
        "reflectivity_index": 0.0,
        "reflectivity_range": 0.5,
        "base_roughness": 0
      },
      "VarFloat3": {
        "refraction_index": [ 2.0, 2.0, 2.0 ],
        "surface_albedo": [ 1.0, 1.0, 1.0 ]
      }
}
"""
Combined reflective and diffuse surface with transparency set according to alpha channel of
``ColorTextures``. See :attr:`plotoptix.materials.m_plastic` and :attr:`plotoptix.materials.m_matt_plastic`
for details.
"""

m_clear_glass = {
      "RadianceProgram": "materials7.ptx::__closesthit__radiance__glass",
      "OcclusionProgram": "materials7.ptx::__closesthit__occlusion",
      "VarUInt": { "flags": 12 },
      "VarFloat": {
        "radiation_length": 0.0,
        "light_emission": 0.0
      },
      "VarFloat3": {
        "refraction_index": [ 1.4, 1.4, 1.4 ],
        "surface_albedo": [ 1.0, 1.0, 1.0 ],
        "subsurface_color": [ 1.0, 1.0, 1.0 ]
      }
    }
"""
Glass, with reflection and refraction simulated. Color components meaning is "attenuation length"
and the color range is <0; inf>. Set ``radiation_length > 0`` to enable sub-surface scattering. It
is supported in background modes :attr:`plotoptix.enums.MissProgram.AmbientAndVolume`,
:attr:`plotoptix.enums.MissProgram.TextureFixed` and :attr:`plotoptix.enums.MissProgram.TextureEnvironment`,
see also :meth:`plotoptix.NpOptiX.set_background_mode`. Use ``subsurface_color`` to set diffuse color of
scattering (RGB components range should be ``<0; 1>``). Volumes can emit light in  ``subsurface_color``
if ``light_emission > 0``.
"""

m_matt_glass = {
      "RadianceProgram": "materials7.ptx::__closesthit__radiance__glass",
      "OcclusionProgram": "materials7.ptx::__closesthit__occlusion",
      "VarUInt": { "flags": 12 },
      "VarFloat": {
        "radiation_length": 0.0,
        "light_emission": 0.0,
        "base_roughness": 0.2
      },
      "VarFloat3": {
        "refraction_index": [ 1.4, 1.4, 1.4 ],
        "surface_albedo": [ 1.0, 1.0, 1.0 ],
        "subsurface_color": [ 1.0, 1.0, 1.0 ]
      }
    }
"""
Glass with surface roughness configured to obtain matt appearance. Color components meaning is
"attenuation length" and the color range is <0; inf>. Set ``radiation_length > 0`` to enable
sub-surface scattering. It is supported in background modes :attr:`plotoptix.enums.MissProgram.AmbientAndVolume`,
:attr:`plotoptix.enums.MissProgram.TextureFixed` and :attr:`plotoptix.enums.MissProgram.TextureEnvironment`,
see also :meth:`plotoptix.NpOptiX.set_background_mode`. Use ``subsurface_color`` to set diffuse color of
scattering (RGB components range should be ``<0; 1>``). Volumes can emit light in  ``subsurface_color``
if ``light_emission > 0``.
"""

m_dispersive_glass = {
      "RadianceProgram": "materials7.ptx::__closesthit__radiance__glass",
      "OcclusionProgram": "materials7.ptx::__closesthit__occlusion",
      "VarUInt": { "flags": 12 },
      "VarFloat": {
        "radiation_length": 0.0,
        "light_emission": 0.0
      },
      "VarFloat3": {
        "refraction_index": [ 1.4, 1.42, 1.45 ],
        "surface_albedo": [ 1.0, 1.0, 1.0 ],
        "subsurface_color": [ 1.0, 1.0, 1.0 ]
      }
    }
"""
Clear glass, with reflection and refraction simulated. Refraction index is varying with the wavelength,
resulting with the light dispersion. Color components meaning is "attenuation length"
and the range is <0; inf>. Set ``radiation_length > 0`` to enable sub-surface scattering. It
is supported in background modes :attr:`plotoptix.enums.MissProgram.AmbientAndVolume`,
:attr:`plotoptix.enums.MissProgram.TextureFixed` and :attr:`plotoptix.enums.MissProgram.TextureEnvironment`,
see also :meth:`plotoptix.NpOptiX.set_background_mode`. Use ``subsurface_color`` to set diffuse color of
scattering (RGB components range should be ``<0; 1>``). Volumes can emit light in  ``subsurface_color``
if ``light_emission > 0``.
"""

m_thin_walled = {
      "RadianceProgram": "materials7.ptx::__closesthit__radiance__glass",
      "OcclusionProgram": "materials7.ptx::__closesthit__occlusion",
      "VarUInt": { "flags": 44 },
      "VarFloat": {
        "radiation_length": 0.0,
        "light_emission": 0.0
      },
      "VarFloat3": {
        "refraction_index": [ 1.9, 1.9, 1.9 ],
      }
    }
"""
Ideal for the soap-like bubbles. Reflection amount depends on the refraction index, however, there is
no refraction on crossing the surface. Reflections can be textured or colorized with the primitive
colors, and the color values range is ``<0; inf)``.
"""

m_shadow_catcher = {
      "RadianceProgram": "materials7.ptx::__closesthit__radiance__shadow_catcher",
      "OcclusionProgram": "materials7.ptx::__closesthit__occlusion",
      "VarUInt": { "flags": 2 },
      "VarFloat": { "base_roughness": 0 }
    }
"""
Diffuse material, transparent except shadowed regions. Colors, textures, roughness can be set
as for other diffuse materials. Useful for preparation of packshot style images. 
"""
