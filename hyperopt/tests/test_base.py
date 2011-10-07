from base import TheanoBanditAlgo

import bandits

def test_TheanoBanditAlgo_on_TwoArms():
    bandit = bandits.TwoArms()
    algo = TheanoBanditAlgo()
    algo.set_bandit(bandit)

    assert algo.recall([]) == ([[]], [[]])

    algo.record([[0]], [[0]])

    assert algo.recall([]) == ([[]], [[]])
    assert algo.recall([0]) == ([[0]], [[0]])

    algo.record([[0, 1, 2]], [[0, 1, 0]])

    assert algo.recall([]) == ([[]], [[]])
    assert algo.recall([0]) == ([[0]], [[0]])
    assert algo.recall([0, 1]) == ([[0, 1]], [[0, 0]])
    assert algo.recall([0, 2]) == ([[0, 1]], [[0, 1]])
    assert algo.recall([0, 3]) == ([[0, 1]], [[0, 0]])


def test_TheanoBanditAlgo_on_EggCarton2():
    bandit = bandits.EggCarton2()
    algo = TheanoBanditAlgo()
    algo.set_bandit(bandit)
    assert len(algo.all_s_idxs) == 6
    assert len(algo.s_idxs) == 3
    assert len(algo.all_s_locs) == 3
    assert algo.all_s_locs == [1, 2, 5]

    if 0:
        nodes = bandit.template.flatten()
        for i, n in enumerate(nodes):
            print i, n
        # 0 - base dict
        # 1 - x (uniform)
        # 2 - hf (one_of)
        # 3 - {'kind': 'raw'}
        # 4 - {'kind': 'negcos'}
        # 5 - amp (uniform)

    assert algo.recall([]) == ([[], [], []], [[], [], []])

    # {x=-5, hf=raw}
    # {x=-10, hf={negcos, amp=.5}
    # {x=-15, hf={negcos, amp=.25}}
    assert algo.record(
            # (x)            (hf)       (amp)  )
            [[0,   1,    2], [0, 1, 2], [1,   2  ]],
            [[-5, -10, -15], [0, 1, 1], [.5, .25 ]])

    assert algo.recall([]) == ([[], [], []], [[], [], []])
    assert algo.recall([0]) == (
            [[0], [0], []],
            [[-5], [0], []])
    assert algo.recall([1]) == (
            [[0], [0], [0]],
            [[-10], [1], [.5]])
    assert algo.recall([2]) == (
            [[0], [0], [0]],
            [[-15], [1], [.25]])

    # {x=-5, hf=raw}
    # {x=-10, hf={negcos, amp=.5}
    # {x=-15, hf={negcos, amp=.25}}
    assert algo.record(
            # (x)            (hf)       (amp)  )
            [[0,  1,  2], [0, 1, 2], [0,   2  ]],
            [[5, 10, 15], [1, 0, 1], [.5, .25 ]])

    assert algo.recall([2,3,4]) == (
            [[0,   1, 2 ], [0, 1, 2], [0, 1]],
            [[-15, 5, 10], [1, 1, 0], [.25, .5]])

# XXX: test suggest()
