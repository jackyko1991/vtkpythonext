#ifndef __yltkObjectFactory_h
#define __yltkObjectFactory_h

#include "yltkObjectFactoryBase.h"

namespace yltk{
	/** \class ObjectFactory
	* \brief Create instances of a class.
	*
	* ObjectFactory is a helper class used to created instances of a
	* class. Object factories are used for instantiation because they allow
	* run-time replacement of a class with a user-supplied version. For
	* example, if you wished to replace an algorithm with your own custom
	* version, or with a hardware-accelerated version, ObjectFactory
	* can be used to do this.
	*
	* This implementation of the object factory is templated and uses RTTI
	* (Run-Time Type Information) to create the name of the class it is to
	* instantiate. (The name may include template type parameters, depending
	* on the class definition.)
	*
	* \ingroup YLTKSystemObjects
	*/
	template <class T>
	class ObjectFactory : public ObjectFactoryBase
	{
	public:
		static typename T::Pointer Create()
		{
			LightObject::Pointer ret = ObjectFactory::CreateInstance(typeid(T).name());
			return dynamic_cast<T*>(ret.GetPointer());
		}
	};
}

#endif