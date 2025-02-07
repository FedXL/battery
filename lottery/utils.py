import random


def get_random_winners(winners_big_count:int, winners_little_count: int, clients_count: int) -> list:
    total = winners_big_count + winners_little_count
    winners = random.sample(range(1, clients_count + 1), total)
    winners_big = winners[:winners_big_count]
    winners_little = winners[winners_big_count:(winners_little_count+winners_big_count)]
    assert len(winners) == (len(winners_big)+len(winners_little)), "Winners count is not equal to total"
    return winners_big, winners_little

