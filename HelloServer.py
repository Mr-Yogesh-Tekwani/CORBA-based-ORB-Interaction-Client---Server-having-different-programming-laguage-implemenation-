import sys
from omniORB import CORBA
import CosNaming, PortableServer
from HelloServant import HelloServant

sys.argv.extend(("-ORBInitRef", "NameService=corbaname::localhost:1050"))

orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
poa = orb.resolve_initial_references("RootPOA")

hello = HelloServant()
servantId = poa.activate_object(hello);

ref = poa.id_to_reference(servantId)

obj = orb.resolve_initial_references("NameService")
rootContext = obj._narrow(CosNaming.NamingContext)


if rootContext is None:
	print("Failed to narrow the root naming context")
	sys.exit(1)


text = "hello"
path = [CosNaming.NameComponent("hello", "")]

try:
    rootContext.bind(path, ref)
    print("Bound the hello object to the naming service")

except CosNaming.NamingContext.AlreadyBound, ex:
    print("Hello object already bound, rebinding new object")
    rootContext.rebind(path, ref)

poa._get_the_POAManager().activate()
print("Python Server active and waiting...")
orb.run()
