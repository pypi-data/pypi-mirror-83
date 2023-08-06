"""The learners module contains core classes and types for defining learner simulations.

This module contains the abstract interface expected for Learner implementations along
with a number of Learner implementations out of the box for testing and baseline comparisons.
"""

import math
import collections

from abc import ABC, abstractmethod
from typing import Any, Callable, Sequence, Tuple, Optional, Dict, cast, Generic, TypeVar, overload, Union, List, Type
from collections import defaultdict
from inspect import signature

import coba.random
import coba.vowpal as VW

from coba.simulations import Context, Action, Reward, Choice, Key
from coba.statistics import OnlineVariance

_C_in = TypeVar('_C_in', bound=Context, contravariant=True)
_A_in = TypeVar('_A_in', bound=Action , contravariant=True)

class Learner(Generic[_C_in, _A_in], ABC):
    """The interface for Learner implementations."""

    @property
    @abstractmethod
    def family(self) -> str:
        """The family of the learner.

        This value is used for descriptive purposes only when creating benchmark results.
        """
        ...

    @property
    @abstractmethod
    def params(self) -> Dict[str,Any]:
        """The parameters used to initialize the learner.

        This value is used for descriptive purposes only when creating benchmark results.
        """
        ...

    @abstractmethod
    def choose(self, key: Key, context: _C_in, actions: Sequence[_A_in]) -> Choice:
        """Choose which action to take.

        Args:
            key: A unique identifier for the interaction that the observed reward 
                came from. This identifier allows learners to share information
                between the choose and learn methods while still keeping the overall 
                learner interface consistent and clean.
            context: The current context. This argument will be None when playing 
                a multi-armed bandit simulation and will contain context features 
                when playing a contextual bandit simulation. Context features could 
                be an individual number (e.g. 1.34), a string (e.g., "hot"), or a 
                tuple of strings and numbers (e.g., (1.34, "hot")) depending on the 
                simulation being played.
            actions: The current set of actions to choose from in the given context. 
                Action sets can be lists of numbers (e.g., [1,2,3,4]), a list of 
                strings (e.g. ["high", "medium", "low"]), or a list of lists such 
                as in the case of movie recommendations (e.g., [["action", "oscar"], 
                ["fantasy", "razzie"]]).

        Returns:
            An integer indicating the index of the selected action in the action set.
        """
        ...

    @abstractmethod
    def learn(self, key: Key, context: _C_in, action: _A_in, reward: Reward) -> None:
        """Learn about the result of an action that was taken in a context.

        Args:
            key: A unique identifier for the interaction that the observed reward 
                came from. This identifier allows learners to share information
                between the choose and learn methods while still keeping the overall 
                learner interface consistent and clean.
            context: The current context. This argument will be None when playing 
                a multi-armed bandit simulation and will contain context features 
                when playing a contextual bandit simulation. Context features could 
                be an individual number (e.g. 1.34), a string (e.g., "hot"), or a 
                tuple of strings and numbers (e.g., (1.34, "hot")) depending on the 
                simulation being played.
            action: The action that was selected to play and observe its reward. 
                An Action can be an individual number (e.g., 2), a string (e.g. 
                "medium"), or a list of some combination of numbers or strings
                (e.g., ["action", "oscar"]).
            reward: the reward received for taking the given action in the given context.
        """
        ...

class LambdaLearner(Learner[_C_in, _A_in]):
    """A Learner implementation that chooses and learns according to provided lambda functions."""

    @overload
    def __init__(self, 
                choose: Callable[[_C_in, Sequence[_A_in]], Choice], 
                learn : Optional[Callable[[_C_in, _A_in, Reward],None]] = None,
                family: str = "Lambda",
                params: Dict[str,Any] = {}) -> None:
        ...
    
    @overload
    def __init__(self, 
                 choose: Callable[[Key, _C_in, Sequence[_A_in]], Choice], 
                 learn : Optional[Callable[[Key, _C_in, _A_in, Reward],None]] = None,
                 family: str = "Lambda",
                 params: Dict[str,Any] = {}) -> None:
        ...

    def __init__(self, choose, learn = None, family: str = "Lambda", params: Dict[str,Any] = {}) -> None:
        """Instantiate LambdaLearner.

        Args:
            chooser: A function matching the `super().choose()` signature. All parameters are passed straight through.
            learner: A function matching the `super().learn()` signature. If provided all parameters are passed
                straight through. If the function isn't provided then no learning occurs.
            family: The family that the lambda learner belongs to.
            params: The parameters used when creating the lambda learner.
        """

        if len(signature(choose).parameters) == 2:
            og_choose = choose
            choose = lambda k,c,A: cast(Callable[[_C_in, Sequence[_A_in]], Choice], og_choose)(c,A)

        if learn is not None and len(signature(learn).parameters) == 3:
            og_learn = learn
            learn = lambda k,c,a,r: cast(Callable[[_C_in, _A_in, Reward], None], og_learn)(c,a,r)

        self._choose = choose
        self._learn  = learn
        self._family = family
        self._params = params

    @property
    def family(self) -> str:
        """The family of the learner.
        
        See the base class for more information
        """
        return self._family

    @property
    def params(self) -> Dict[str, Any]:
        """The parameters of the learner.
        
        See the base class for more information
        """
        return self._params

    def choose(self, key: Key, context: _C_in, actions: Sequence[_A_in]) -> Choice:
        """Choose via the provided lambda function.

        Args:
            key: The key identifying the interaction we are choosing for.
            context: The context we're currently in. See the base class for more information.
            actions: The actions to choose from. See the base class for more information.

        Returns:
            The index of the selected action. See the base class for more information.
        """

        return self._choose(key, context, actions)

    def learn(self, index: int, context: _C_in, action: _A_in, reward: Reward) -> None:
        """Learn via the optional lambda function or learn nothing without a lambda function.

        Args:
            key: The key identifying the interaction this observed reward came from.
            context: The context we're learning about. See the base class for more information.
            action: The action that was selected in the context. See the base class for more information.
            reward: The reward that was gained from the action. See the base class for more information.
        """
        if self._learn is None:
            pass
        else:
            self._learn(index, context,action,reward)

class RandomLearner(Learner[Context, Action]):
    """A Learner implementation that selects an action at random and learns nothing."""

    def __init__(self, seed: Optional[int] = None):
        self._random = coba.random.Random(seed)

    @property
    def family(self) -> str:
        """The family of the learner.

        See the base class for more information
        """  
        return "random"

    @property
    def params(self) -> Dict[str, Any]:
        """The parameters of the learner.
        
        See the base class for more information
        """
        return { }

    def choose(self, key: Key, context: Context, actions: Sequence[Action]) -> Choice:
        """Choose a random action from the action set.
        
        Args:
            key: The key identifying the interaction we are choosing for.
            context: The context we're currently in. See the base class for more information.
            actions: The actions to choose from. See the base class for more information.

        Returns:
            The index of the selected action. See the base class for more information.
        """
        return self._random.randint(0, len(actions)-1)

    def learn(self, key: Key, context: Context, action: Action, reward: Reward) -> None:
        """Learns nothing.

        Args:
            key: The key identifying the interaction this observed reward came from.
            context: The context we're learning about. See the base class for more information.
            action: The action that was selected in the context. See the base class for more information.
            reward: The reward that was gained from the action. See the base class for more information.
        """
        pass
 
class EpsilonLearner(Learner[Context, Action]):
    """A learner using epsilon-greedy searching while smoothing observations into a context/context-action lookup table.

    Remarks:
        This algorithm does not use any function approximation to attempt to generalize observed rewards.
    """

    def __init__(self, epsilon: float, include_context: bool = False, seed: Optional[int] = None) -> None:
        """Instantiate an EpsilonLearner.

        Args:
            epsilon: A value between 0 and 1. We explore with probability epsilon and exploit otherwise.
            init: Our initial guess of the expected rewards for all context-action pairs.
            include_context: If true lookups are a function of context-action otherwise they are a function of action.
        """

        self._epsilon         = epsilon
        self._include_context = include_context
        self._random          = coba.random.Random(seed)

        self._N: Dict[Tuple[Context, Action], int            ] = defaultdict(int)
        self._Q: Dict[Tuple[Context, Action], Optional[float]] = defaultdict(int)

    @property
    def family(self) -> str:
        """The family of the learner.

        See the base class for more information
        """
        if self._include_context:
            return "cb_epsilongreedy"
        else:
            return "bandit_epsilongreedy"

    @property
    def params(self) -> Dict[str, Any]:
        """The parameters of the learner.
        
        See the base class for more information
        """
        return {"epsilon": self._epsilon }

    def choose(self, key: Key, context: Context, actions: Sequence[Action]) -> Choice:
        """Choose greedily with probability 1-epsilon. Choose a randomly with probability epsilon.

        Args:
            key: The key identifying the interaction we are choosing for.
            context: The context we're currently in. See the base class for more information.
            actions: The actions to choose from. See the base class for more information.

        Returns:
            The index of the selected action. See the base class for more information.
        """
        if(self._random.random() <= self._epsilon): return self._random.randint(0,len(actions)-1)

        keys        = [ self._key(context,action) for action in actions ]
        values      = [ self._Q[key] for key in keys ]
        max_value   = None if set(values) == {None} else max(v for v in values if v is not None)
        max_indexes = [i for i in range(len(values)) if values[i]==max_value]

        return self._random.choice(max_indexes)

    def learn(self, key: Key, context: Context, action: Action, reward: Reward) -> None:
        """Smooth the observed reward into our current estimate of either E[R|S,A] or E[R|A].

        Args:
            key: The key identifying the interaction this observed reward came from.
            context: The context we're learning about. See the base class for more information.
            action: The action that was selected in the context. See the base class for more information.
            reward: The reward that was gained from the action. See the base class for more information.
        """

        sa_key = self._key(context,action)
        alpha  = 1/(self._N[sa_key]+1)

        old_Q = cast(float, 0 if self._Q[sa_key] is None else self._Q[sa_key])

        self._Q[sa_key] = (1-alpha) * old_Q + alpha * reward
        self._N[sa_key] = self._N[sa_key] + 1

    def _key(self, context: Context, action: Action) -> Tuple[Context,Action]:
        return (context, action) if self._include_context else (None, action)

class UcbTunedLearner(Learner[Context, Action]):
    """This is an implementation of Auer et al. (2002) UCB1-Tuned algorithm.

    References:
        Auer, Peter, Nicolo Cesa-Bianchi, and Paul Fischer. "Finite-time analysis of 
        the multiarmed bandit problem." Machine learning 47.2-3 (2002): 235-256.
    """
    def __init__(self, seed: int = None):
        """Instantiate a UcbTunedLearner."""

        self._init_a: int = 0
        self._t     : int = 0
        self._s     : Dict[Action,int] = {}
        self._m     : Dict[Action,float] = {}
        self._v     : Dict[Action,OnlineVariance] = defaultdict(OnlineVariance)
        
        self._random = coba.random.Random(seed)

    @property
    def family(self) -> str:
        """The family of the learner.

        See the base class for more information
        """
        return "bandit_UCB"

    @property
    def params(self) -> Dict[str, Any]:
        """The parameters of the learner.
        
        See the base class for more information
        """
        return { }

    def choose(self, key: Key, context: Context, actions: Sequence[Action]) -> Choice:
        """Choose an action greedily by the upper confidence bound estimates.

        Args:
            key: The key identifying the interaction we are choosing for.
            context: The context we're currently in. See the base class for more information.
            actions: The actions to choose from. See the base class for more information.

        Returns:
            The index of the selected action. See the base class for more information.
        """
        #we initialize by playing every action once
        if self._init_a < len(actions):
            self._init_a += 1
            return self._init_a-1

        else:
            values      = [ self._m[a] + self._Avg_R_UCB(a) if a in self._m else None for a in actions ]
            max_value   = None if set(values) == {None} else max(v for v in values if v is not None)
            max_indexes = [i for i in range(len(values)) if values[i]==max_value]
            return self._random.choice(max_indexes)

    def learn(self, key: Key, context: Context, action: Action, reward: Reward) -> None:
        """Smooth the observed reward into our current estimate of E[R|A].

        Args:
            key: The key identifying the interaction this observed reward came from.
            context: The context we're learning about. See the base class for more information.
            action: The action that was selected in the context. See the base class for more information.
            reward: The reward that was gained from the action. See the base class for more information.
        """
        if action not in self._s:
            self._s[action] = 1
        else:
            self._s[action] += 1

        if action not in self._m:
            self._m[action] = reward
        else:
            self._m[action] = (1-1/self._s[action]) * self._m[action] + 1/self._s[action] * reward

        self._t         += 1
        self._s[action] += 1
        self._v[action].update(reward)

    def _Avg_R_UCB(self, action: Action) -> float:
        """Produce the estimated upper confidence bound (UCB) for E[R|A].

        Args:
            action: The action for which we want to retrieve UCB for E[R|A].

        Returns:
            The estimated UCB for E[R|A].

        Remarks:
            See the beginning of section 4 in the algorithm's paper for this equation.
        """
        ln = math.log; n = self._t; n_j = self._s[action]; V_j = self._Var_R_UCB(action)

        return math.sqrt(ln(n)/n_j * min(1/4,V_j))

    def _Var_R_UCB(self, action: Action) -> float:
        """Produce the upper confidence bound (UCB) for Var[R|A].

        Args:
            action: The action for which we want to retrieve UCB for Var[R|A].

        Returns:
            The estimated UCB for Var[R|A].

        Remarks:
            See the beginning of section 4 in the algorithm's paper for this equation.
        """
        ln = math.log; t = self._t; s = self._s[action]; var = self._v[action].variance

        return var + math.sqrt(2*ln(t)/s)    
    
class VowpalLearner(Learner[Context, Action]):
    """A learner using Vowpal Wabbit's contextual bandit command line interface.

    Remarks:
        This learner requires that the Vowpal Wabbit package be installed. This package can be
        installed via `pip install vowpalwabbit`. To learn more about solving contextual bandit
        problems with Vowpal Wabbit see https://vowpalwabbit.org/tutorials/contextual_bandits.html
        and https://github.com/VowpalWabbit/vowpal_wabbit/wiki/Contextual-Bandit-algorithms.
    """

    @overload
    def __init__(self, *, epsilon: float, is_adf: bool = True, seed:int = None) -> None:
        """Instantiate a VowpalLearner.
        Args:
            epsilon: A value between 0 and 1. If provided exploration will follow epsilon-greedy.
        """
        ...

    @overload
    def __init__(self, *, bag: int, is_adf: bool = True, seed:int = None) -> None:
        """Instantiate a VowpalLearner.
        Args:
            bag: An integer value greater than 0. This value determines how many separate policies will be
                learned. Each policy will be learned from bootstrap aggregation, making each policy unique. 
                For each choice one policy will be selected according to a uniform distribution and followed.
        """
        ...

    @overload
    def __init__(self, *, cover: int, seed:int = None) -> None:
        """Instantiate a VowpalLearner.
        Args:
            cover: An integer value greater than 0. This value value determines how many separate policies will be
                learned. These policies are learned in such a way to explicitly optimize policy diversity in order
                to control exploration. For each choice one policy will be selected according to a uniform distribution
                and followed. For more information on this algorithm see Agarwal et al. (2014).
        References:
            Agarwal, Alekh, Daniel Hsu, Satyen Kale, John Langford, Lihong Li, and Robert Schapire. "Taming 
            the monster: A fast and simple algorithm for contextual bandits." In International Conference on 
            Machine Learning, pp. 1638-1646. 2014.
        """
        ...

    @overload
    def __init__(self, *, softmax:float, seed:int = None) -> None:
        """Instantiate a VowpalLearner.
        Args:
            softmax: An exploration parameter with 0 indicating uniform exploration is desired and infinity
                indicating that no exploration is desired (aka, greedy action selection only). For more info
                see `lambda` at https://github.com/VowpalWabbit/vowpal_wabbit/wiki/Contextual-Bandit-algorithms.
        """
        ...

    @overload
    def __init__(self,
        learning: VW.cb_explore,
        exploration: Union[VW.epsilongreedy, VW.bagging, VW.cover], *, seed:int = None) -> None:
        ...
    
    @overload
    def __init__(self,
        learning: VW.cb_explore_adf = VW.cb_explore_adf(),
        exploration: Union[VW.epsilongreedy, VW.softmax, VW.bagging] = VW.epsilongreedy(0.025), 
        *, 
        seed:int = None) -> None:
        ...

    def __init__(self, 
        learning: Union[VW.cb_explore,VW.cb_explore_adf] = VW.cb_explore_adf(),
        exploration: Union[VW.epsilongreedy, VW.softmax, VW.bagging, VW.cover] = VW.epsilongreedy(0.025),
        **kwargs) -> None:
        """Instantiate a VowpalLearner with the requested VW learner and exploration."""

        self._learning: Union[VW.cb_explore,VW.cb_explore_adf]
        self._exploration: Union[VW.epsilongreedy, VW.softmax, VW.bagging, VW.cover]

        if 'epsilon' in kwargs:
            self._learning    = VW.cb_explore_adf() if kwargs.get('is_adf',True) else VW.cb_explore()
            self._exploration = VW.epsilongreedy(kwargs['epsilon'])

        elif 'softmax' in kwargs:
            self._learning   = VW.cb_explore_adf()
            self._exploration = VW.softmax(kwargs['softmax'])

        elif 'bag' in kwargs:
            self._learning = VW.cb_explore_adf() if kwargs.get('is_adf',True) else VW.cb_explore()
            self._exploration = VW.bagging(kwargs['bag'])
        
        elif 'cover' in kwargs:
            self._learning = VW.cb_explore()
            self._exploration = VW.cover(kwargs['cover'])
        
        else:
            self._learning = learning
            self._exploration = exploration

        self._probs: Dict[Key, float] = {}
        self._actions = self._new_actions(learning)

        self._vw = VW.pyvw_Wrapper(learning.formatter, seed=kwargs.get('seed', None))
    
    @property
    def family(self) -> str:
        """The family of the learner.

        See the base class for more information
        """
        return f"vw_{self._learning.__class__.__name__}_{self._exploration.__class__.__name__}"
    
    @property
    def params(self) -> Dict[str, Any]:
        """The parameters of the learner.
        
        See the base class for more information
        """        
        return {**self._learning.params(), **self._exploration.params()}

    def choose(self, key: Key, context: Context, actions: Sequence[Action]) -> Choice:
        """Choose an action according to the VowpalWabbit parameters passed into the contructor.

        Args:
            key: The key identifying the interaction we are choosing for.
            context: The context we're currently in. See the base class for more information.
            actions: The actions to choose from. See the base class for more information.

        Returns:
        
            The index of the selected action. See the base class for more information.
        """

        if not self._vw.created:
            self._vw.create(self._learning.flags(actions) + " " + self._exploration.flags())        

        choice, prob = self._vw.choose(context, actions)

        self._set_actions(key,actions)
        self._probs[key] = prob
        
        if isinstance(self._learning, VW.cb_explore):
            return actions.index(self._actions[choice])
        else:
            return choice

    def learn(self, key: Key, context: Context, action: Action, reward: Reward) -> None:
        """Learn from the obsered reward for the given context action pair.

        Args:
            key: The key identifying the interaction this observed reward came from.
            context: The context we're learning about. See the base class for more information.
            action: The action that was selected in the context. See the base class for more information.
            reward: The reward that was gained from the action. See the base class for more information.
        """

        actions = self._get_actions(key)
        prob = self._probs[key]        

        self._vw.learn(prob, actions, context, action, reward)

    def _new_actions(self, learning) -> Any:
        if isinstance(learning, VW.cb_explore):
            return []
        else:
            return {}

    def _set_actions(self, key, actions) -> None:
        if self._actions == []:
            self._actions = actions

        if isinstance(self._actions, collections.MutableMapping):
            self._actions[key] = actions

    def _get_actions(self, key) -> Sequence[Action]:
        if isinstance(self._actions, collections.MutableMapping) :
            return self._actions.pop(key)
        else:
            return self._actions