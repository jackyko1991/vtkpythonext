#include "yltkToken.h"
#include "yltkSimpleFastMutexLock.h"

#include <iostream>


namespace yltk
{

	/** The counter for providing pseudo-unique identifiers for tokens */
	Token::IdentifierType Token::m_IdentifierCounter = 1;

	/** Used for mutex locking */
	static ::yltk::SimpleFastMutexLock    TokenMutex;

	/** Constructor */ 
	Token::Token()
	{
		/** Start mutual exclusion section. This prevent race conditions when
		* multiple threads are creating Tokens simultaneously */
		TokenMutex.Lock();

		/** When the IdentifierCounter rolls over (reaches it maximum value and
		* restars from zero) the Uniqueness of identifiers can no longer be
		* guaranted. */
		this->m_Identifier  = m_IdentifierCounter++;

		TokenMutex.Unlock();
	}

	/** Destructor */
	Token::~Token()
	{
	}

	/** Print Self function */
	void Token::PrintSelf( std::ostream& os, yltk::Indent indent ) const
	{
		os << indent << "RTTI typeinfo:   " << typeid( *this ).name() << std::endl;
		os << indent << "Identifier: " << this->m_Identifier << std::endl;
	}

	void Token::Print(std::ostream& os, yltk::Indent indent) const
	{
		os << indent << "Token" << " (" << this << ")\n";
		this->PrintSelf(os, indent.GetNextIndent());
	}

	std::ostream& operator<<(std::ostream& os, const Token& o)
	{
		o.Print(os, 0);
		return os;
	}

} // end namespace igstk