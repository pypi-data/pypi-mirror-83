from . import Havok

hk = Havok.from_file('/home/kreny/botw_havok_testfiles/u/Physics/RigidBody/Obj_TreeConiferous_C/Obj_TreeConiferous_C_03.hkrb')
hk.deserialize()

hk1 = Havok.from_dict(hk.as_dict())
hk1.to_wiiu()
hk1.serialize()
bytesnew=hk1.to_bytes()

hk.serialize()
bytesold=hk.to_bytes()

print(bytesold == bytesnew)

print()
