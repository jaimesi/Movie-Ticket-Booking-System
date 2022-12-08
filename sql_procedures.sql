use movie_final;

-- for customer to view their tickets
delimiter $$
create procedure showTicket(customer_id_p int)
begin
	with t as (select ticket_id, customer_id, show_id, seat_no from ticket where customer_id = customer_id_p),
    c as (select customer_id, first_name, last_name from customer where customer_id = customer_id_p)
		select t.ticket_id as ticket_id, c.first_name as first_name, c.last_name as last_name, m.movie_name as movie_name, 
		s.auditorium_id as auditorium, s.showing_date as showing_date, s.showing_time as showing_time, t.seat_no as no_seat
			from t join c on t.customer_id = c.customer_id
			join showing as s on s.show_id = t.show_id
			join movie as m on m.movie_id = s.movie_id;
end$$
delimiter ;

drop procedure showTicket;

insert into ticket (customer_id, show_id, seat_no) values (1, 1, 2);
call showTicket(1);

-- for customer and manager to delete the ticket
delimiter $$
create procedure deleteTicket(ticket_id_p int)
begin
	delete from ticket where ticket_id = ticket_id_p;
end$$
delimiter ;

-- for manager to view all tickets
delimiter $$
create procedure showAllTicket()
begin
	select * from ticket;
end$$
delimiter ;

-- check if the customer already exists
delimiter $$
create function customerExist(email_p varchar(64))
returns int
deterministic
reads sql data
begin
	declare result int;
    select count(*) into result from customer where email = email_p;
    return result;
end$$
delimiter ;
select customerExist('customer@test.com');

-- customer sign up
delimiter $$
create procedure addCustomer(email_p varchar(64), password_p varchar(64), first_name_p varchar(64), last_name_p varchar(64))
begin
	insert into customer (email, customer_password, first_name, last_name) values 
		(email_p, password_p, first_name_p, last_name_p);
end$$
delimiter ;

-- get today's movie pricing (for manager to add showings)
delimiter $$
create function getPriceId(day_p varchar(10), type_p enum("2D", "3D", "IMAX"))
returns int
deterministic
reads sql data
begin
	declare result int;
    select price_id into result from pricing where pricing_day = day_p and pricing_type = type_p;
    return result;
end$$
delimiter ;

-- manager add showing
delimiter $$
create procedure addShowing(movie_id_p int, pricing_id_p int, auditorium_id_p int, 
	showing_type_p enum("2D", "3D", "IMAX"), showing_date_p date, showing_time_p char(5))
begin
	insert into showing(movie_id, pricing_id, auditorium_id, showing_type, showing_date, showing_time)
		values (movie_id_p, pricing_id_p, auditorium_id_p, showing_type_p, showing_date_p, showing_time_p);
end$$
delimiter ;

-- manager update showing (only update price, date, time, auditorium)
delimiter $$
create procedure updateShowing(show_id_p int, pricing_id_p int, auditorium_id_p int, showing_date_p date, showing_time_p char(5))
begin
	update showing
    set pricing_id = pricing_id_p,
		auditorium_id = auditorium_id_p,
        showing_date = showing_date_p,
        showing_time = showing_time_p
	where show_id = show_id_p;
end$$
delimiter ;

-- manager delete showing
delimiter $$
create procedure deleteShowing(show_id_p int)
begin
	delete from showing where show_id = show_id_p;
end$$
delimiter ;

-- check if customer email and password matches
delimiter $$
create function customerSignin(email_p varchar(64), password_p varchar(64))
returns int
deterministic
reads sql data
begin
	declare result int;
	select count(*) into result from customer where email = email_p and customer_password = password_p;
    return result;
end$$
delimiter ;

-- check if manager username and password matches
delimiter $$
create function managerSignin(username_p varchar(64), password_p varchar(64))
returns int
deterministic
reads sql data
begin
	declare result int;
	select count(*) into result from manager where username = username_p and manager_password = password_p;
    return result;
end$$
delimiter ;

drop procedure showShowing;
delimiter $$
create procedure showShowing(movie_name_p varchar(64))
begin
	with m as (select movie_id from movie where movie_name = movie_name_p)
    select s.show_id, s.showing_time, s.showing_date, p.price
    from showing as s join m on s.movie_id = m.movie_id
		join pricing as p on p.pricing_id = s.pricing_id;
end$$
delimiter ;
call showShowing('Black Panther: Wakanda Forever');

-- add ticket for customer
delimiter $$
create procedure addTicket(customer_id_p int, show_id_p int, seat_no_p int)
begin
	insert ticket (customer_id, show_id, seat_no) values
		(customer_id_p, show_id_p, seat_no_p);
end$$
delimiter ;

INSERT INTO `showing` VALUES (1,505642,3,2,1,'IMAX','12:00','2022-11-28'),(2,505642,2,1,1,'3D','14:30','2022-11-28'),(3,800939,1,1,1,'2D','21:15','2022-11-28'),(4,505642,3,2,1,'IMAX','10:30','2022-11-29'),(5,505642,3,2,1,'IMAX','17:45','2022-11-29');

