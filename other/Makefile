# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: averon <averon@student.42Mulhouse.fr>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/03/10 10:20:15 by stissera          #+#    #+#              #
#    Updated: 2023/05/04 16:13:12 by averon           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME		=	spider
CC			=	c++
FLAGS		=	-Wall -Werror -Wextra -std=c++11
LDFLAGS		=	-L/Users/faventur/goinfre/.brew/opt/curl/lib -lcurl
LIBLINKS	=	-I./includes
LIBLINKS	+=	-I/Users/faventur/goinfre/.brew/opt/curl/include

FILES		=	main.cpp
RM			=	rm -rf
SRCS		=	$(addprefix ./, $(FILES))
OBJS		=	$(SRCS:%.cpp=%.o)

$(NAME)		:	$(OBJS)
				$(CC) $(LDFLAGS) $(FLAGS) $(OBJS) -o $(NAME)

.cpp.o		:
	$(CC) $(FLAGS) $(LIBLINKS) -c $< -o ${<:.cpp=.o}

all			:	$(NAME)

clean:
	$(RM) $(OBJS)

fclean		:	clean
				$(RM) $(NAME)

re			:	fclean all

.PHONY		:	all clean fclean re