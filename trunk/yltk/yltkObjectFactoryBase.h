#ifndef __yltkObjectFactoryBase_h
#define __yltkObjectFactoryBase_h

#include "yltkObject.h"
#include "yltkCreateObjectFunction.h"
#include <list>
#include <vector>
#include <string>

namespace yltk{
	/** \class ObjectFactoryBase
	* \brief Create instances of classes using an object factory.
	*
	* ObjectFactoryBase is used to create yltk objects. The base class
	* ObjectFactoryBase contains a static method CreateInstance() that is
	* used to create yltk objects from the list of registerd ObjectFactoryBase
	* sub-classes.  The first time CreateInstance() is called, all dll's or
	* shared libraries in the environment variable ITK_AUTOLOAD_PATH are loaded
	* into the current process.  The C function itkLoad is called on each dll.
	* itkLoad should return an instance of the factory sub-class implemented in
	* the shared library. YLTK_AUTOLOAD_PATH is an environment variable
	* containing a colon separated (semi-colon on win32) list of paths.
	*
	* This can be use to overide the creation of any object in YLTK. 
	*
	* \ingroup YLTKSystemObjects
	*/
	class OverRideMap;

	class ObjectFactoryBase: public Object
	{
	public:
		/** Standard class typedefs. */
		typedef ObjectFactoryBase        Self;
		typedef Object                   Superclass;
		typedef SmartPointer<Self>       Pointer;
		typedef SmartPointer<const Self> ConstPointer;

		/** Run-time type information (and related methods). */
		yltkTypeMacro(ObjectFactoryBase, Object);

		/** Create and return an instance of the named yltk object.
		* Each loaded ObjectFactoryBase will be asked in the order
		* the factory was in the YLTK_AUTOLOAD_PATH.  After the
		* first factory returns the object no other factories are asked. */
		static LightObject::Pointer CreateInstance(const char* yltkclassname);

		/** Create and return all possible instances of the named yltk object.
		* Each loaded ObjectFactoryBase will be asked in the order
		* the factory was in the YLTK_AUTOLOAD_PATH.  All created objects
		* will be returned in the list. */
		static std::list<LightObject::Pointer>CreateAllInstance(const char* yltkclassname);

		/** Re-check the YLTK_AUTOLOAD_PATH for new factory libraries.
		* This calls UnRegisterAll before re-loading. */
		static void ReHash(); 

		/** Register a factory so it can be used to create yltk objects. */
		static void RegisterFactory(ObjectFactoryBase* );

		/** Remove a factory from the list of registered factories. */
		static void UnRegisterFactory(ObjectFactoryBase*);

		/** Unregister all factories. */
		static void UnRegisterAllFactories();

		/** Return the list of all registered factories.  This is NOT a copy,
		* do not remove items from this list! */
		static std::list<ObjectFactoryBase*> GetRegisteredFactories();

		/** All sub-classes of ObjectFactoryBase should must return the version of 
		* YLTK they were built with.  This should be implemented with the macro
		* YLTK_SOURCE_VERSION and NOT a call to Version::GetYLTKSourceVersion.
		* As the version needs to be compiled into the file as a string constant.
		* This is critical to determine possible incompatible dynamic factory loads. */
		virtual const char* GetYLTKSourceVersion(void) const = 0;

		/** Return a descriptive string describing the factory. */
		virtual const char* GetDescription(void) const = 0;

		/** Return a list of classes that this factory overrides. */
		virtual std::list<std::string> GetClassOverrideNames();

		/** Return a list of the names of classes that override classes. */
		virtual std::list<std::string> GetClassOverrideWithNames();

		/** Return a list of descriptions for class overrides. */
		virtual std::list<std::string> GetClassOverrideDescriptions();

		/** Return a list of enable flags. */
		virtual std::list<bool> GetEnableFlags();

		/** Set the Enable flag for the specific override of className. */
		virtual void SetEnableFlag(bool flag, const char* className, const char* subclassName);

		/** Get the Enable flag for the specific override of className. */
		virtual bool GetEnableFlag(const char* className, const char* subclassName);

		/** Set all enable flags for the given class to 0.  This will
		* mean that the factory will stop producing class with the given
		* name. */
		virtual void Disable(const char* className);

		/** This returns the path to a dynamically loaded factory. */
		const char* GetLibraryPath();

		/** \class OverrideInformation
		* \brief Internal implementation class for ObjectFactorBase. */
		struct OverrideInformation
		{
			std::string m_Description;
			std::string m_OverrideWithName;
			bool m_EnabledFlag;
			CreateObjectFunctionBase::Pointer m_CreateObject;
		};

	protected:
		virtual void PrintSelf(std::ostream& os, Indent indent) const;

		/** Register object creation information with the factory. */
		void RegisterOverride(const char* classOverride,
			const char* overrideClassName,
			const char* description,
			bool enableFlag,
			CreateObjectFunctionBase* createFunction);

		/** This method is provided by sub-classes of ObjectFactoryBase.
		* It should create the named yltk object or return 0 if that object
		* is not supported by the factory implementation. */
		virtual LightObject::Pointer CreateObject(const char* yltkclassname );

		ObjectFactoryBase();
		virtual ~ObjectFactoryBase();

	private:
		OverRideMap* m_OverrideMap;

		ObjectFactoryBase(const Self&); //purposely not implemented
		void operator=(const Self&); //purposely not implemented

		/** Initialize the static members of ObjectFactoryBase.   RegisterDefaults
		* is called here. */
		static void Initialize();

		/** Register default factories which are not loaded at run time. */
		static void RegisterDefaults();

		/** Load dynamic factories from the YLTK_AUTOLOAD_PATH */
		static void LoadDynamicFactories();

		/** Load all dynamic libraries in the given path */
		static void LoadLibrariesInPath( const char*);

		/** list of registered factories */
		static std::list<ObjectFactoryBase*>* m_RegisteredFactories; 

		/** Member variables for a factory set by the base class
		* at load or register time */
		void*         m_LibraryHandle;
		unsigned long m_LibraryDate;
		std::string   m_LibraryPath;
	};
}

#endif