#ifndef __yltkStateMachineState_h
#define __yltkStateMachineState_h

#include "yltkToken.h"

namespace yltk
{


	/** \class StateMachineState
	*  \brief Generic implementation of the State in a State Machine model.
	*
	*  This class provides a generic representation of a State.  It is  intended
	*  to be derived in order to implement specific states an to enforce the
	*  following characteristics on the behavior of the State Machine:
	*
	*  \li Preclude the definition of two states with the same name.
	*  \li Provide high performance search for the presence of a particular state.
	*  \li Provide descriptive text-like definition of each state.
	*
	*  These characteristics are enforced by taking advantage of natural checks
	*  performed by the compiler. In particular, the uniqueness of the State name
	*  will be enforced by making every state to be an C++ variable. The compiler
	*  will produce errors as a result of any attempt to repeat the name of a
	*  variable inside the same namespace.
	*
	*
	*  \sa StateMachine
	*  \sa StateMachineInput
	*  \sa Token
	*  \sa StateMachineAction
	*
	*/

	template< class T >
	class StateMachineState : public Token
	{
	public:

		typedef StateMachineState Self;
		typedef Token             Superclass;

		/** Constructor. It initializes all the member variables */
		StateMachineState() {}

		/** Destructor */
		virtual ~StateMachineState() {}

	protected:

		/** Print the object information in a stream. */
		virtual void PrintSelf( std::ostream& os, yltk::Indent indent ) const
		{
			Superclass::PrintSelf(os, indent);
		}
	};

} // end namespace yltk

#endif
